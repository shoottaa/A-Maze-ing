from typing import List, Tuple


NORTH = 0x1  # 0001
EAST = 0x2  # 0010
SOUTH = 0x4 # 0100
WEST = 0x8 # 1000


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

    """ Affichage ASCII temporaire pour tester.
    L'affichage est un peu buggé car les murs sont des deux côtés
    et là ça n'en affiche qu'un seul. """
    def temp_print_grid(self) -> None:
        for y in range(self.height):
            top = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                top += "+"
                if cell.has_wall(NORTH):
                    top += "---"
                else:
                    top += "   "
            top += "+"
            print(top)

            mid = ""
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.has_wall(WEST):
                    mid += "|"
                else:
                    mid += " "
                if (x, y) == self.entry:
                    mid += " E "
                elif (x, y) == self.exit_pos:
                    mid += " X "
                else:
                    mid += "   "
            if self.grid[y][self.width - 1].has_wall(EAST):
                mid += "|"
            else:
                mid += " "
            print(mid)

        bot = ""
        for x in range(self.width):
            cell = self.grid[self.height - 1][x]
            bot += "+"
            if cell.has_wall(SOUTH):
                bot += "---"
            else:
                bot += "   "
        bot += "+"
        print(bot)


if __name__ == "__main__":
    m = Maze(5, 4, (0, 0), (4, 2))

    m.temp_print_grid()
    print()

    m.get_cell(1, 0).remove_wall(WEST)
    m.get_cell(1, 0).remove_wall(SOUTH)
    m.get_cell(1, 1).remove_wall(NORTH)
    m.get_cell(1, 1).remove_wall(EAST)
    m.get_cell(2, 1).remove_wall(WEST)

    m.temp_print_grid()
    print()
