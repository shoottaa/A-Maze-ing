from typing import List, Set, Tuple


NORTH = 0x1  # 0001
EAST = 0x2  # 0010
SOUTH = 0x4  # 0100
WEST = 0x8  # 1000

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
    """Represente une cellule en 4 bits des murs."""
    def __init__(self, x: int, y: int) -> None:
        """Initialise une cellule en x/y avec les 4 murs fermes"""
        self.x = x
        self.y = y
        self.walls = 0xF

    def has_wall(self, direction: int) -> bool:
        """Renvoie True si le mur dans la direction donnee est ferme"""
        return bool(self.walls & direction)

    def remove_wall(self, direction: int) -> None:
        """Supprime le mur dans la direction donnee"""
        self.walls &= ~direction

    def to_hex(self) -> str:
        """Renvoie le caractere hex des bits des murs"""
        return format(self.walls, 'X')


class Maze:
    """Represente la grille de toutes les cellules"""
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int],
                 exit_pos: Tuple[int, int]) -> None:
        """Initialise la grille avec tous les murs fermes
            width: Nombre de colonnes
            height: Nombre de lignes
            entry: Coordonnees x/y de l'entree
            exit_pos: Coordonnees x/y de la sortie"""
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
        self.pattern_cells: Set[Tuple[int, int]] = set()

    def get_cell(self, x: int, y: int) -> Cell:
        """Renvoie la cellule (objet Cell) en x/y"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise ValueError(f"Cell ({x},{y}) OOB")
        return self.grid[y][x]
