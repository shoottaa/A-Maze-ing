from src.maze import Maze

DIGIT_4 = [
    [1, 0, 0, 1, 0],
    [1, 0, 0, 1, 0],
    [1, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
]

DIGIT_2 = [
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
]

GAP = 2


def pattern_42(maze: Maze) -> None:
    h = len(DIGIT_4)
    w4 = len(DIGIT_4[0])
    w2 = len(DIGIT_2[0])
    total_w = w4 + GAP + w2

    # Le pattern ne s'affiche qu'à partir de 21x16
    if maze.width < 21 or maze.height < 16:
        maze.pattern_cells = set()
        print("Pattern 42 : Taille insuffisante (minimum 21x16)")
        return

    x0 = (maze.width - total_w) // 2
    y0 = (maze.height - h) // 2
    x2 = x0 + w4 + GAP

    maze.stamp_y0 = y0
    maze.stamp_h = h

    # Construction de l'ensemble des positions du pattern
    pattern_cells = set()
    for row in range(h):
        for col in range(w4):
            if DIGIT_4[row][col]:
                pattern_cells.add((x0 + col, y0 + row))
        for col in range(w2):
            if DIGIT_2[row][col]:
                pattern_cells.add((x2 + col, y0 + row))

    maze.pattern_cells = pattern_cells

    # Ferme tous les murs des cellules du pattern
    for (px, py) in pattern_cells:
        maze.get_cell(px, py).walls = 0xF

    # Restaure les murs ouverts
    directions = [
        (0, -1, 0x4, 0x1),  # Nord du pattern : ferme mur SUD
        (0, +1, 0x1, 0x4),  # Sud du pattern : ferme mur NORD
        (-1, 0, 0x2, 0x8),  # Ouest du pattern : restaure son mur EST
        (+1, 0, 0x8, 0x2),  # Est du pattern : restaure son mur OUEST
    ]

    for (px, py) in pattern_cells:
        for dx, dy, _pattern_wall, neighbor_wall in directions:
            nx, ny = px + dx, py + dy
            if 0 <= nx < maze.width and 0 <= ny < maze.height:
                if (nx, ny) not in pattern_cells:
                    maze.get_cell(nx, ny).walls |= neighbor_wall
