from typing import List, Tuple


NORTH = 0x1  # 0001
EAST = 0x2  # 0010
SOUTH = 0x4 # 0100
WEST = 0x8 # 1000

# (offset_x, offset_y, mur, lettre)
DIRECTIONS = [
    (0, -1, NORTH, "N"),
    (1,  0, EAST,  "E"),
    (0,  1, SOUTH, "S"),
    (-1, 0, WEST,  "W"),
]

OPPOSITE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST:  WEST,
    WEST:  EAST,
}


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = 0xF  # 1111 = les 4 murs fermes

    def has_wall(self, direction: int) -> bool:
        # AND bitwise : garde uniquement le bit de la direction
        # Ex: 1101 & 0010 = 0000 -> False -> pas de mur est
        return bool(self.walls & direction)

    def remove_wall(self, direction: int) -> None:
        # Inverse les bits, & enlève le bit de la direction
        # Ex: ~0010 = 1101, 1111 & 1101 = 1101 -> mur est cassé
        self.walls &= ~direction

    def to_hex(self) -> str:
        return format(self.walls, 'X')


class Maze:
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int],
                 exit_pos: Tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_pos = exit_pos
        self.grid: List[List[Cell]] = []
        for y in range(height):
            row: List[Cell] = []
            for x in range(width):
                row.append(Cell(x, y))
            self.grid.append(row)
        self.pattern_cells: set = set()

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError(f"Cell ({x},{y}) OOB")
        return self.grid[y][x]