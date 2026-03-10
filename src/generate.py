import random
from src.maze import Maze
from src.pattern import pattern_42


def get_neighbors(maze: Maze, x: int, y: int) -> list:
    # Renvoie les 4 voisins possibles 
    neighbors = []
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
    # Casse le mur des 2 cotes
    cell_from = maze.get_cell(from_x, from_y)
    cell_to = maze.get_cell(to_x, to_y)
    if to_x > from_x:
        cell_from.remove_wall(0x2)   # EAST
        cell_to.remove_wall(0x8)     # WEST
    elif to_x < from_x:
        cell_from.remove_wall(0x8)   # WEST
        cell_to.remove_wall(0x2)     # EAST
    elif to_y > from_y:
        cell_from.remove_wall(0x4)   # SOUTH
        cell_to.remove_wall(0x1)     # NORTH
    else:
        cell_from.remove_wall(0x1)   # NORTH
        cell_to.remove_wall(0x4)     # SOUTH


"""
DFS : Recursive backtracker
1. On part de l'entrée
2. On choisit un voisin au hasard
3. On casse le mur
4. On avance vers cette case
5. On retourne à l'étape 2 jusqu'à ce que toutes les cellules voisines soient visitées
6. On revient en arrière jusqu'à trouver une cellule avec des voisins non visités
"""


def generate_maze(maze: Maze, seed: int = 42,
                  perfect: bool = True) -> None:
    pattern_42(maze)
    random.seed(seed)

    visited = set()  # les cellules deja visitees
    stack = [maze.entry]  # le chemin cellule par cellule
    visited.add(maze.entry)

    while stack:
        x, y = stack[-1]  # Dernier element de la stack

        unvisited = []  # Liste des voisins non visités
        for neighbor in get_neighbors(maze, x, y):
            if neighbor not in visited and neighbor not in maze.pattern_cells:
                unvisited.append(neighbor)

        if unvisited:
            next_x, next_y = random.choice(unvisited)  # On choisit un voisin au hasard
            open_between(maze, x, y, next_x, next_y)   # On casse le mur
            visited.add((next_x, next_y))
            stack.append((next_x, next_y))  # On avance
        else:
            # Aucun voisin libre, on recule d'une case
            stack.pop()


    if not perfect:
        # On cherche tous les murs encore debout pour en casser 10%
        walls = []
        for row in range(maze.height):
            for col in range(maze.width):
                cell = maze.get_cell(col, row)
                if col < maze.width - 1 and cell.has_wall(0x2):  # EAST
                    walls.append((col, row, col + 1, row))
                if row < maze.height - 1 and cell.has_wall(0x4):  # SOUTH
                    walls.append((col, row, col, row + 1))
                if col > 0 and cell.has_wall(0x8):  # WEST
                    walls.append((col, row, col - 1, row))
                if row > 0 and cell.has_wall(0x1):  # NORTH
                    walls.append((col, row, col, row - 1))
        nb = max(1, len(walls) // 10)
        to_remove = random.sample(walls, min(nb, len(walls)))
        for from_x, from_y, to_x, to_y in to_remove:
            open_between(maze, from_x, from_y, to_x, to_y)
