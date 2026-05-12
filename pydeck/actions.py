import os
import subprocess
import webbrowser

from .models import Shortcut


def execute_shortcut(shortcut: Shortcut) -> str | None:
    try:
        if shortcut.action_type == "command":
            subprocess.Popen(shortcut.action_value, shell=True)
        elif shortcut.action_type in ("program", "file"):
            os.startfile(shortcut.action_value)
        elif shortcut.action_type == "url":
            webbrowser.open(shortcut.action_value)
    except Exception as ex:
        return str(ex)
    return None


def allowed_extensions(action_type: str) -> list[str] | None:
    if action_type == "program":
        return ["exe", "bat", "cmd", "com", "lnk"]
    return None
