import random
from typing import List, Tuple
from mazegen.maze import Maze, EAST, SOUTH, WEST, NORTH
from .pattern import pattern_42


def get_neighbors(maze: Maze, x: int,
                  y: int) -> List[Tuple[int, int]]:
    """Renvoie les coordonnees des voisins de x/y"""
    neighbors: List[Tuple[int, int]] = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < maze.width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < maze.height - 1:
        neighbors.append((x, y + 1))
    return neighbors


def open_between(maze: Maze, from_x: int, from_y: int,
                 to_x: int, to_y: int) -> None:
    """Casse le mur entre deux cellules des deux cotes"""
    cell_from = maze.get_cell(from_x, from_y)
    cell_to = maze.get_cell(to_x, to_y)
    if to_x > from_x:
        cell_from.remove_wall(EAST)
        cell_to.remove_wall(WEST)
    elif to_x < from_x:
        cell_from.remove_wall(WEST)
        cell_to.remove_wall(EAST)
    elif to_y > from_y:
        cell_from.remove_wall(SOUTH)
        cell_to.remove_wall(NORTH)
    else:
        cell_from.remove_wall(NORTH)
        cell_to.remove_wall(SOUTH)


def generate_maze(maze: Maze, seed: int = 42,
                  perfect: bool = True) -> None:
    """Genere un labyrinthe avec le Recursive Backtracker (DFS)
        maze: L'instance du labyrinthe a remplir
        seed: Seed aleatoire
        perfect: Si True genere un labyrinthe parfait"""
    pattern_42(maze)
    random.seed(seed)

    visited = set()
    stack = [maze.entry]
    visited.add(maze.entry)

    while stack:
        x, y = stack[-1]

        unvisited: List[Tuple[int, int]] = []
        for neighbor in get_neighbors(maze, x, y):
            if (neighbor not in visited
                    and neighbor not in maze.pattern_cells):
                unvisited.append(neighbor)

        if unvisited:
            next_x, next_y = random.choice(unvisited)
            open_between(maze, x, y, next_x, next_y)
            visited.add((next_x, next_y))
            stack.append((next_x, next_y))
        else:
            stack.pop()

    if not perfect:
        walls: List[Tuple[int, int, int, int]] = []
        for row in range(maze.height):
            for col in range(maze.width):
                if (col, row) in maze.pattern_cells:
                    continue
                cell = maze.get_cell(col, row)
                east = (col + 1, row)
                south = (col, row + 1)
                if (col < maze.width - 1
                        and cell.has_wall(EAST)
                        and east not in maze.pattern_cells):
                    walls.append((col, row, col + 1, row))
                if (row < maze.height - 1
                        and cell.has_wall(SOUTH)
                        and south not in maze.pattern_cells):
                    walls.append((col, row, col, row + 1))
        nb = max(1, len(walls) // 10)
        to_remove = random.sample(
            walls, min(nb, len(walls))
        )
        for from_x, from_y, to_x, to_y in to_remove:
            open_between(maze, from_x, from_y, to_x, to_y)

        # Corrige les zones 3x3 ouvertes en fermant un mur
        for row in range(maze.height - 2):
            for col in range(maze.width - 2):
                open_area = True
                for y in range(3):
                    for x in range(3):
                        cell = maze.get_cell(col + x, row + y)
                        if x < 2 and cell.has_wall(EAST):
                            open_area = False
                        if y < 2 and cell.has_wall(SOUTH):
                            open_area = False
                if open_area:
                    cell_from = maze.get_cell(col + 1, row + 1)
                    cell_to = maze.get_cell(col + 2, row + 1)
                    cell_from.walls |= EAST
                    cell_to.walls |= WEST
