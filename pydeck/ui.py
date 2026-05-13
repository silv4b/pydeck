import asyncio
from pathlib import Path

import flet as ft

from .models import Shortcut
from .theme import (
    COMPACT_SIZE,
    P_ACCENT,
    P_LIGHT,
    P_PRIMARY,
    P_SURFACE,
)


def build_top_bar(config_mode: bool, on_toggle, on_compact, on_reset) -> ft.Row:
    return ft.Row(
        [
            ft.Text("PyDeck", size=18, weight=ft.FontWeight.BOLD, color=P_LIGHT),
            ft.Container(expand=True),
            ft.IconButton(
                icon=ft.Icons.CIRCLE_OUTLINED,
                icon_color=P_LIGHT,
                tooltip="Modo Compacto (Ctrl+Shift+C)",
                on_click=lambda _: on_compact(),
            ),
            ft.IconButton(
                icon=ft.Icons.CHECK_ROUNDED if config_mode else ft.Icons.EDIT_ROUNDED,
                icon_color=P_LIGHT,
                tooltip="Config (Ctrl+E)",
                on_click=lambda _: on_toggle(),
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE_SWEEP,
                icon_color=ft.Colors.RED_400,
                tooltip="Resetar configurações",
                on_click=lambda _: on_reset(),
            ),
        ]
    )


def build_card(
    shortcut: Shortcut,
    config_mode: bool,
    on_click,
    on_edit,
    on_delete,
) -> ft.Container:
    inner = ft.Column(
        [
            ft.Text(shortcut.icon, size=32, text_align=ft.TextAlign.CENTER),
            ft.Text(
                shortcut.title,
                size=12,
                color=P_LIGHT,
                text_align=ft.TextAlign.CENTER,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    if config_mode:
        edit_btn = ft.Container(
            content=ft.Icon(ft.Icons.EDIT_ROUNDED, size=14, color=P_LIGHT),
            width=24,
            height=24,
            border_radius=12,
            bgcolor="#80000000",
            alignment=ft.Alignment(0, 0),
            top=4,
            right=4,
            on_click=lambda _, s=shortcut: on_edit(s),
        )
        del_btn = ft.Container(
            content=ft.Icon(ft.Icons.DELETE_ROUNDED, size=14, color=ft.Colors.RED_400),
            width=24,
            height=24,
            border_radius=12,
            bgcolor="#80000000",
            alignment=ft.Alignment(0, 0),
            top=4,
            left=4,
            on_click=lambda _, s=shortcut: on_delete(s),
        )
        inner = ft.Stack([inner, edit_btn, del_btn], alignment=ft.Alignment(0, 0))

    return ft.Container(
        content=inner,
        bgcolor=shortcut.color,
        border_radius=12,
        ink=True,
        on_click=lambda _, s=shortcut: on_click(s),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_IN_OUT),
        expand=True,
    )


def build_add_button(on_add) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.ADD_ROUNDED, size=40, color=P_LIGHT),
                ft.Text("Adicionar", size=12, color=P_LIGHT),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        border=ft.Border(
            left=ft.BorderSide(2, P_ACCENT),
            top=ft.BorderSide(2, P_ACCENT),
            right=ft.BorderSide(2, P_ACCENT),
            bottom=ft.BorderSide(2, P_ACCENT),
        ),
        border_radius=12,
        ink=True,
        expand=True,
        on_click=lambda _: on_add(),
    )


def build_edit_form(
    shortcut: Shortcut,
    is_new: bool,
    page: ft.Page,
    file_picker: ft.FilePicker,
    on_save,
    on_cancel,
) -> ft.Column:
    title_tf = ft.TextField(label="Título", value=shortcut.title)
    icon_tf = ft.TextField(label="Ícone (emoji)", value=shortcut.icon)
    type_dd = ft.Dropdown(
        label="Tipo de Ação",
        options=[
            ft.DropdownOption("command", "Comando"),
            ft.DropdownOption("program", "Programa"),
            ft.DropdownOption("file", "Arquivo"),
            ft.DropdownOption("url", "URL"),
        ],
        value=shortcut.action_type,
    )
    value_tf = ft.TextField(
        label="Valor",
        value=shortcut.action_value,
        multiline=True,
        expand=True,
    )
    browse_btn = ft.IconButton(
        icon=ft.Icons.FOLDER_OPEN,
        icon_color=P_ACCENT,
        tooltip="Procurar",
        on_click=lambda _: asyncio.create_task(
            pick_file(page, file_picker, value_tf, type_dd)
        ),
    )
    value_row = ft.Row([value_tf, browse_btn], spacing=4, tight=True)
    color_tf = ft.TextField(
        label="Cor (hex)", value=shortcut.color, hint_text="#1E88E5"
    )

    def save(_):
        shortcut.title = title_tf.value or ""
        shortcut.icon = icon_tf.value or ""
        shortcut.action_type = type_dd.value or "command"
        shortcut.action_value = value_tf.value or ""
        shortcut.color = color_tf.value or "#1E88E5"
        on_save(shortcut, is_new)

    def cancel(_):
        on_cancel()

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "Novo Atalho" if is_new else "Editar Atalho",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=P_PRIMARY,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE_ROUNDED,
                        icon_color=P_LIGHT,
                        tooltip="Cancelar",
                        on_click=cancel,
                    ),
                ]
            ),
            ft.Divider(color=P_SURFACE),
            title_tf,
            icon_tf,
            type_dd,
            value_row,
            color_tf,
            ft.Container(expand=True),
            ft.Row(
                [
                    ft.Container(expand=True),
                    ft.OutlinedButton("Cancelar", on_click=cancel),
                    ft.FilledButton(
                        "Salvar",
                        on_click=save,
                        bgcolor=P_ACCENT,
                        color=P_LIGHT,
                    ),
                ]
            ),
        ],
        expand=True,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )


def build_delete_dialog(shortcut: Shortcut, on_confirm, on_cancel) -> ft.AlertDialog:
    dlg = ft.AlertDialog(
        title=ft.Text("Excluir Atalho", color=P_PRIMARY),
        bgcolor=P_SURFACE,
        content=ft.Text(
            f'Tem certeza que deseja excluir "{shortcut.title}"?', color=P_LIGHT
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: on_cancel(dlg)),
            ft.FilledButton(
                "Excluir",
                on_click=lambda _: on_confirm(dlg),
                color=P_LIGHT,
                bgcolor=ft.Colors.RED_700,
            ),
        ],
    )
    return dlg


def build_snackbar(page: ft.Page, message: str) -> ft.SnackBar:
    snack = ft.SnackBar(
        ft.Text(f"Erro: {message}"),
        bgcolor=ft.Colors.RED_900,
        open=True,
    )
    snack.on_dismiss = lambda _: page.overlay.remove(snack)
    return snack


_ICON_PATH = str(Path(__file__).resolve().parent.parent / "assets" / "pydeck_icon.png")


def build_compact_view(
    page: ft.Page, on_restore, on_drag_end=None
) -> ft.WindowDragArea:
    return ft.WindowDragArea(
        content=ft.Container(
            content=ft.Image(
                src=_ICON_PATH,
                fit="fill",
                gapless_playback=True,
                width=COMPACT_SIZE,
                height=COMPACT_SIZE,
            ),
            width=COMPACT_SIZE,
            height=COMPACT_SIZE,
            on_click=lambda _: on_restore(),
        ),
        width=COMPACT_SIZE,
        height=COMPACT_SIZE,
        on_drag_end=lambda _: on_drag_end() if on_drag_end else None,
    )


async def pick_file(
    page: ft.Page,
    file_picker: ft.FilePicker,
    value_tf: ft.TextField,
    type_dd: ft.Dropdown,
) -> None:
    if type_dd.value not in ("program", "file"):
        return
    allowed = (
        ["exe", "bat", "cmd", "com", "lnk"] if type_dd.value == "program" else None
    )
    files = await file_picker.pick_files(
        dialog_title="Selecione o arquivo",
        allowed_extensions=allowed,
        allow_multiple=False,
    )
    if files:
        value_tf.value = files[0].path or ""
        page.update()
