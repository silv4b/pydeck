import asyncio

import flet as ft

from . import actions
from . import ui
from .config import ConfigManager
from .models import Shortcut
from .theme import (
    COMPACT_EXTRA,
    COMPACT_SIZE,
    EDIT_FORM_HEIGHT,
    GRID_SPACING,
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
        self.compact_mode = False
        self._saved_window = {}
        self._saved_height = WINDOW_HEIGHT
        self._saved_bgcolor = None
        self._saved_window_bgcolor = None
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
        if e.ctrl and e.shift and e.key == "C":
            self._toggle_compact_mode()
        elif e.ctrl and e.key == "E":
            self._toggle_config_mode()

    def _toggle_config_mode(self):
        self.config_mode = not self.config_mode
        self._build_ui()

    def _toggle_compact_mode(self):
        if self.compact_mode:
            return
        p = self.page
        self._saved_window = {
            "left": p.window.left,
            "top": p.window.top,
            "width": p.window.width,
            "height": p.window.height,
            "always_on_top": p.window.always_on_top,
        }
        self.compact_mode = True
        self._saved_bgcolor = p.bgcolor
        self._saved_window_bgcolor = p.window.bgcolor
        p.controls.clear()
        p.spacing = 0
        p.padding = 0
        p.window.bgcolor = "transparent"
        p.bgcolor = "transparent"
        p.window.frameless = True
        p.window.width = COMPACT_SIZE
        p.window.height = COMPACT_SIZE + COMPACT_EXTRA
        p.window.min_width = COMPACT_SIZE
        p.window.min_height = COMPACT_SIZE + COMPACT_EXTRA
        p.window.always_on_top = True
        p.window.resizable = False
        cfg = self.cm.config
        if cfg.compact_x is not None and cfg.compact_y is not None:
            p.window.left = cfg.compact_x
            p.window.top = cfg.compact_y
        else:
            asyncio.create_task(p.window.center())
        p.add(
            ui.build_compact_view(p, self._restore_from_compact, self._save_compact_pos)
        )
        p.update()

    def _save_compact_pos(self):
        p = self.page
        self.cm.config.compact_x = int(p.window.left or 0)
        self.cm.config.compact_y = int(p.window.top or 0)
        self.cm.save()

    def _restore_from_compact(self):
        if not self.compact_mode:
            return
        p = self.page
        self.compact_mode = False

        self.cm.config.compact_x = int(p.window.left or 0)
        self.cm.config.compact_y = int(p.window.top or 0)
        self.cm.save()

        p.controls.clear()
        p.window.bgcolor = self._saved_window_bgcolor
        p.bgcolor = self._saved_bgcolor or P_BG
        self.main_col.spacing = 10
        p.padding = 12
        p.window.frameless = False
        p.window.left = self._saved_window.get("left")
        p.window.top = self._saved_window.get("top")
        p.window.width = self._saved_window.get("width", WINDOW_WIDTH)
        p.window.height = self._saved_window.get("height", WINDOW_HEIGHT)
        p.window.min_width = 0
        p.window.min_height = 0
        p.window.always_on_top = self._saved_window.get(
            "always_on_top", self.cm.config.always_on_top
        )
        p.window.resizable = False
        p.add(self.main_col)
        self._build_ui()

    def _on_reset_config(self):
        def confirm(dlg):
            self.cm.reset_to_defaults()
            dlg.open = False
            dlg.update()
            self._build_ui()

        def cancel(dlg):
            dlg.open = False
            dlg.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Resetar Configurações"),
            bgcolor="#44475A",
            content=ft.Text(
                "Tem certeza que deseja resetar todas as configurações "
                "e atalhos para os valores padrão?",
                color="#F8F8F2",
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: cancel(dlg)),
                ft.FilledButton(
                    "Resetar",
                    on_click=lambda _: confirm(dlg),
                    color="#F8F8F2",
                    bgcolor=ft.Colors.RED_700,
                ),
            ],
        )
        self.page.show_dialog(dlg)

    def _build_ui(self):
        n = len(self.cm.config.shortcuts) + (1 if self.config_mode else 0)
        rows = max(1, (n + 3) // 4)
        rows = min(rows, 5)
        w = int(self.page.window.width or WINDOW_WIDTH)
        tile = tile_size(w)
        h = window_height(tile, rows)

        self.main_col.controls.clear()
        self.main_col.controls.append(
            ui.build_top_bar(
                self.config_mode,
                self._toggle_config_mode,
                self._toggle_compact_mode,
                self._on_reset_config,
            )
        )
        grid_height = rows * tile + (rows - 1) * GRID_SPACING
        grid = ft.GridView(
            height=grid_height,
            runs_count=4,
            child_aspect_ratio=1.0,
            spacing=12,
            run_spacing=12,
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

        self.page.window.resizable = True
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
