from typing import Dict, List, Optional, Tuple
from mazegen.maze import Maze, DIRECTIONS


def solve(maze: Maze) -> Optional[str]:
    """Trouve le plus court chemin de l'entree a la sortie via BFS
    Retourne: Directions (Ex: NNNEESSW) ou None"""
    start = maze.entry
    end = maze.exit_pos

    visited = {start}
    queue = [start]
    parent: Dict[
        Tuple[int, int], Tuple[Tuple[int, int], str]
    ] = {}

    while queue:
        x, y = queue.pop(0)

        if (x, y) == end:
            return reconstruct(parent, start, end)

        cell = maze.get_cell(x, y)
        for dir_x, dir_y, wall, letter in DIRECTIONS:
            next_x, next_y = x + dir_x, y + dir_y
            if (next_x, next_y) in visited:
                continue
            if cell.has_wall(wall):
                continue
            if next_x < 0 or next_x >= maze.width:
                continue
            if next_y < 0 or next_y >= maze.height:
                continue
            visited.add((next_x, next_y))
            parent[(next_x, next_y)] = ((x, y), letter)
            queue.append((next_x, next_y))

    return None


def solve_cells(maze: Maze) -> List[Tuple[int, int]]:
    """Renvoie la liste des cellules x/y du plus court chemin"""
    path_str = solve(maze)
    if not path_str:
        return []
    convert_letter = {
        "N": (0, -1), "S": (0, 1),
        "E": (1, 0), "W": (-1, 0),
    }
    x, y = maze.entry
    cells: List[Tuple[int, int]] = [(x, y)]
    # Applique les deplacements et ajoute la pos a la liste
    for letter in path_str:
        dir_x, dir_y = convert_letter[letter]
        x += dir_x
        y += dir_y
        cells.append((x, y))
    return cells


def reconstruct(
    parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]],
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> str:
    """Reconstruit la chaine de directions depuis le dictionnaire parent"""
    letters: List[str] = []
    current = end

    while current != start:
        prev, letter = parent[current]
        letters.append(letter)
        current = prev

    letters.reverse()
    return "".join(letters)


def write_output(maze: Maze, filepath: str) -> None:
    """Ecrit le labyrinthe et la solution dans un fichier au format du sujet"""
    path_str = solve(maze)
    if path_str is None:
        path_str = ""

    try:
        with open(filepath, 'w') as f:
            for y in range(maze.height):
                row = ""
                for x in range(maze.width):
                    row += maze.get_cell(x, y).to_hex()
                f.write(row + "\n")

            f.write("\n")
            f.write(f"{maze.entry[0]},{maze.entry[1]}\n")
            f.write(f"{maze.exit_pos[0]},{maze.exit_pos[1]}\n")
            f.write(path_str + "\n")
    except OSError as e:
        print(f"Erreur d'écriture: {e}")
