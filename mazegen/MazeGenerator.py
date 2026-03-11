from typing import Tuple
from ..src.maze import Maze
from ..src.generate import generate_maze


class MazeGenerator:
    def __init__(self,
                 width: int,
                 height: int,
                 entry: Tuple[int, int] = (0, 0),
                 exit_pos: Tuple[int, int] | None = None,
                 seed: int = 42,
                 perfect: bool = True):

        self.maze = Maze(width, height, entry, exit_pos)
        generate_maze(self.maze, seed=seed, perfect=perfect)

        def get_maze(self) -> Maze:
            """Renvoie l'objet Maze."""
            return self.maze

        def get_grid(self):
            """Renvoie la grille."""
            return self.maze.grid
