import asyncio

import flet as ft

from . import actions
from . import ui
from .config import ConfigManager
from .models import Shortcut
from .theme import (
    EDIT_FORM_HEIGHT,
    OVERHEAD_HEIGHT,
    P_BG,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    tile_size,
    window_height,
)


class PyDeckApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.cm = ConfigManager()
        self.config_mode = False
        self._saved_height = WINDOW_HEIGHT
        self.main_col = ft.Column(expand=True, spacing=10)
        self.page.add(self.main_col)
        self.file_picker = ft.FilePicker()
        self.page.services.append(self.file_picker)
        self._setup_page()
        self._build_ui()

    def _setup_page(self):
        p = self.page
        p.title = "PyDeck"
        p.window.width = WINDOW_WIDTH
        p.window.height = WINDOW_HEIGHT
        p.window.always_on_top = self.cm.config.always_on_top
        p.window.resizable = False
        p.window.maximizable = False
        p.theme_mode = ft.ThemeMode.DARK
        p.bgcolor = P_BG
        p.padding = 12
        p.on_keyboard_event = self._on_keyboard
        asyncio.create_task(p.window.center())

    def _on_keyboard(self, e: ft.KeyboardEvent):
        if e.ctrl and e.key == "E":
            self._toggle_config_mode()

    def _toggle_config_mode(self):
        self.config_mode = not self.config_mode
        self._build_ui()

    def _build_ui(self):
        self.main_col.controls.clear()
        self.main_col.controls.append(
            ui.build_top_bar(self.config_mode, self._toggle_config_mode)
        )

        grid = ft.GridView(
            expand=True,
            runs_count=4,
            child_aspect_ratio=1.0,
            spacing=12,
            run_spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )
        for s in self.cm.config.shortcuts:
            grid.controls.append(
                ui.build_card(
                    s,
                    self.config_mode,
                    self._on_card_click,
                    self._edit_shortcut,
                    self._delete_shortcut,
                )
            )
        if self.config_mode:
            grid.controls.append(ui.build_add_button(self._add_shortcut))
        self.main_col.controls.append(grid)

        n = len(grid.controls)
        rows = max(1, (n + 3) // 4)
        rows = min(rows, 5)
        w = self.page.window.width or WINDOW_WIDTH
        tile = tile_size(w)
        h = window_height(tile, rows)
        min_h = OVERHEAD_HEIGHT + 2 * tile + 12
        self.page.window.min_height = min_h
        self.page.window.height = h

        self.page.update()

    def _on_card_click(self, shortcut: Shortcut):
        if self.config_mode:
            self._edit_shortcut(shortcut)
            return
        error = actions.execute_shortcut(shortcut)
        if error:
            self.page.overlay.append(ui.build_snackbar(self.page, error))
            self.page.update()

    def _edit_shortcut(self, shortcut: Shortcut, is_new: bool = False):
        self.main_col.controls.clear()
        self._saved_height = self.page.window.height
        self.main_col.controls.append(
            ui.build_edit_form(
                shortcut,
                is_new,
                self.page,
                self.file_picker,
                self._on_form_save,
                self._on_form_cancel,
            )
        )
        self.page.window.height = EDIT_FORM_HEIGHT
        self.page.update()

    def _add_shortcut(self):
        self._edit_shortcut(Shortcut(), is_new=True)

    def _on_form_save(self, shortcut: Shortcut, is_new: bool):
        if is_new:
            self.cm.add_shortcut(shortcut)
        else:
            self.cm.update_shortcut(shortcut)
        self.page.window.height = self._saved_height
        self._build_ui()

    def _on_form_cancel(self):
        self.page.window.height = self._saved_height
        self._build_ui()

    def _delete_shortcut(self, shortcut: Shortcut):
        def confirm(dlg):
            self.cm.delete_shortcut(shortcut.id)
            dlg.open = False
            dlg.update()
            self._build_ui()

        def cancel(dlg):
            dlg.open = False
            dlg.update()

        dlg = ui.build_delete_dialog(shortcut, confirm, cancel)
        self.page.show_dialog(dlg)


def main():
    ft.app(target=PyDeckApp)
