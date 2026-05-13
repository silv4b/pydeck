import json
import os

from .models import Config, Shortcut
from .os_utils import is_windows


def _config_dir() -> str:
    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.join(os.path.expanduser("~"), ".config")
    path = os.path.join(base, "pydeck")
    os.makedirs(path, exist_ok=True)
    return path


def _default_shortcuts() -> list[Shortcut]:
    if is_windows():
        return [
            Shortcut(
                title="Bloco de Notas",
                icon="📝",
                action_type="program",
                action_value="notepad.exe",
                color="#4CAF50",
            ),
            Shortcut(
                title="Calculadora",
                icon="🧮",
                action_type="program",
                action_value="calc.exe",
                color="#FF9800",
            ),
            Shortcut(
                title="Terminal",
                icon="💻",
                action_type="program",
                action_value="cmd.exe",
                color="#2196F3",
            ),
            Shortcut(
                title="Google",
                icon="🌐",
                action_type="url",
                action_value="https://google.com",
                color="#9C27B0",
            ),
        ]
    return [
        Shortcut(
            title="Navegador",
            icon="🌐",
            action_type="command",
            action_value="xdg-open https://google.com",
            color="#4CAF50",
        ),
        Shortcut(
            title="Terminal",
            icon="💻",
            action_type="command",
            action_value="gnome-terminal",
            color="#2196F3",
        ),
        Shortcut(
            title="Calculadora",
            icon="🧮",
            action_type="command",
            action_value="gnome-calculator",
            color="#FF9800",
        ),
        Shortcut(
            title="Google",
            icon="🌐",
            action_type="url",
            action_value="https://google.com",
            color="#9C27B0",
        ),
    ]


def _defaults() -> Config:
    return Config(shortcuts=_default_shortcuts())


class ConfigManager:
    def __init__(self, config_path: str | None = None):
        self.config_path = config_path or os.path.join(_config_dir(), "config.json")
        self.config = self.load()

    def load(self) -> Config:
        if not os.path.exists(self.config_path):
            cfg = _defaults()
            self.config = cfg
            self.save()
            return cfg

        with open(self.config_path, encoding="utf-8") as f:
            data = json.load(f)

        return Config(
            grid_columns=data.get("grid_columns", 4),
            button_size=data.get("button_size", 100),
            always_on_top=data.get("always_on_top", True),
            compact_x=data.get("compact_x"),
            compact_y=data.get("compact_y"),
            shortcuts=[Shortcut(**s) for s in data.get("shortcuts", [])],
        )

    def save(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "grid_columns": self.config.grid_columns,
                    "button_size": self.config.button_size,
                    "always_on_top": self.config.always_on_top,
                    "compact_x": self.config.compact_x,
                    "compact_y": self.config.compact_y,
                    "shortcuts": [
                        {
                            "id": s.id,
                            "title": s.title,
                            "icon": s.icon,
                            "action_type": s.action_type,
                            "action_value": s.action_value,
                            "color": s.color,
                        }
                        for s in self.config.shortcuts
                    ],
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    def add_shortcut(self, s: Shortcut) -> None:
        self.config.shortcuts.append(s)
        self.save()

    def update_shortcut(self, s: Shortcut) -> None:
        for i, x in enumerate(self.config.shortcuts):
            if x.id == s.id:
                self.config.shortcuts[i] = s
                break
        self.save()

    def delete_shortcut(self, sid: str) -> None:
        self.config.shortcuts = [s for s in self.config.shortcuts if s.id != sid]
        self.save()

    def reset_to_defaults(self) -> None:
        self.config = _defaults()
        self.save()
