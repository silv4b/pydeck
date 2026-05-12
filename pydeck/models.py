import uuid
from dataclasses import dataclass, field


@dataclass
class Shortcut:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = "Novo Atalho"
    icon: str = "⚡"
    action_type: str = "command"
    action_value: str = ""
    color: str = "#1E88E5"


@dataclass
class Config:
    grid_columns: int = 4
    button_size: int = 100
    always_on_top: bool = True
    shortcuts: list = field(default_factory=list)
