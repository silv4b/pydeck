# Colors
P_BG = "#282A36"
P_PRIMARY = "#BD93F9"
P_ACCENT = "#FF79C6"
P_SURFACE = "#44475A"
P_DARK = "#282A36"
P_LIGHT = "#F8F8F2"

# Layout
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 460
EDIT_FORM_HEIGHT = 480
PADDING = 12
GRID_COLUMNS = 4
GRID_SPACING = 12
OVERHEAD_HEIGHT = 110
MIN_GRID_ROWS = 2
MAX_GRID_ROWS = 5

COMPACT_SIZE = 100


def tile_size(window_width: int) -> int:
    return (
        window_width - PADDING * 2 - GRID_SPACING * (GRID_COLUMNS - 1)
    ) // GRID_COLUMNS


def grid_height(tile: int, rows: int) -> int:
    return rows * tile + (rows - 1) * GRID_SPACING


def window_height(tile: int, rows: int) -> int:
    return OVERHEAD_HEIGHT + grid_height(tile, rows)
