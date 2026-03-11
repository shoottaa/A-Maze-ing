from typing import Tuple
from .generate import generate_maze
from .solve import solve
from .maze import Maze


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
        return self.maze

    def get_grid(self):
        return self.maze.grid

    def maze_solve(self):
        return solve(self.maze)
