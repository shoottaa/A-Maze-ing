from src.maze import Maze, DIRECTIONS


"""
BFS : Breadth-First Search
1. On part de l'entrée, on l'ajoute dans la file
2. On prend le premier élément de la file
3. Pour chaque voisin accessible :
- Si pas encore visité, on l'ajoute dans la file
- On note d'où on vient (parent) et la direction prise
- Dès qu'on atteint la sortie, on remonte les parents
"""


def solve(maze: Maze) -> None:
    start = maze.entry
    end = maze.exit_pos

    
    visited = {start}  # Ex: {(0,0), (1,0), (2,0)}
    queue = [start]  # Ex: [(1,0), (0,1)] = cellules à traiter (first in first out)
    parent = {}  # Ex: {(1,0): ((0,0), "E")}

    while queue:
        x, y = queue.pop(0)  # On prend le premier de la file

        if (x, y) == end:  # Sortie de fonction si on trouve la sortie
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
            parent[(next_x, next_y)] = ((x, y), letter)  # On note le parent
            queue.append((next_x, next_y))  # On ajoute dans la file

    return None


def solve_cells(maze: Maze) -> list[tuple]:
    path_str = solve(maze)
    if not path_str:
        return []
    convert_letter = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
    x, y = maze.entry
    cells = [(x, y)]
    for letter in path_str:
        dir_x, dir_y = convert_letter[letter]
        x += dir_x
        y += dir_y
        cells.append((x, y))
    return cells


def reconstruct(parent: dict, start: tuple, end: tuple) -> str:
    letters = []
    current = end

    while current != start:
        prev, letter = parent[current]
        letters.append(letter)
        current = prev

    letters.reverse()  # On a remonté à l'envers, on inverse
    return "".join(letters)



def write_output(maze: Maze, filepath: str) -> None:
    # Écrit le maze au format du sujet
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
        print(f"Could not write file output.")


if __name__ == "__main__":
    # python3 -m src.solve
    # python3 output_validator.py maze.txt
    from src.generate import generate_maze

    m = Maze(20, 15, (0, 0), (19, 14))
    generate_maze(m, seed=42, perfect=True)
    write_output(m, "maze.txt")
