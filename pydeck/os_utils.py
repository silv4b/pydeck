import os
import subprocess
import webbrowser


def is_windows() -> bool:
    return os.name == "nt"


def is_linux() -> bool:
    return os.name == "posix"


def open_path(path: str) -> None:
    if is_windows():
        os.startfile(path)
    else:
        subprocess.Popen(["xdg-open", path])


def open_url(url: str) -> None:
    if is_windows():
        webbrowser.open(url)
    else:
        subprocess.Popen(["xdg-open", url])


def run_command(command: str) -> None:
    subprocess.Popen(command, shell=True)


def picker_extensions(action_type: str) -> list[str] | None:
    if action_type != "program":
        return None
    if is_windows():
        return ["exe", "bat", "cmd", "com", "lnk"]
    return ["sh", "desktop", "AppImage"]
