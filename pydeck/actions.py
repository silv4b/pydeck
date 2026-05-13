from .models import Shortcut
from .os_utils import open_path, open_url, run_command


def execute_shortcut(shortcut: Shortcut) -> str | None:
    try:
        if shortcut.action_type == "command":
            run_command(shortcut.action_value)
        elif shortcut.action_type in ("program", "file"):
            open_path(shortcut.action_value)
        elif shortcut.action_type == "url":
            open_url(shortcut.action_value)
    except Exception as ex:
        return str(ex)
    return None
