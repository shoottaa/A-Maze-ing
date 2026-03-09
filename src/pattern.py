from src.maze import Maze, DIRECTIONS, OPPOSITE

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
    """Ajoute un pattern 42 au centre, en fermant les murs des cellules"""
    pattern_height = len(DIGIT_4)
    digit4_width = len(DIGIT_4[0])
    digit2_width = len(DIGIT_2[0])
    total_width = digit4_width + GAP + digit2_width

    # Le pattern ne s'affiche qu'à partir de 21x16
    if maze.width < 21 or maze.height < 16:
        maze.pattern_cells = set()
        return

    # Centre le pattern horizontalement
    digit4_start_x = (maze.width - total_width) // 2
    # Positionne le 2 à droite du 4
    digit2_start_x = digit4_start_x + digit4_width + GAP
    # Centre verticalement le pattern et devient la pos initiale du 4 et du 2
    start_y = (maze.height - pattern_height) // 2

    # Construction de l'ensemble des positions du pattern
    pattern_cells = set()
    for row in range(pattern_height):
        for col in range(digit4_width):
            if DIGIT_4[row][col]:
                pattern_cells.add((digit4_start_x + col, start_y + row))
        for col in range(digit2_width):
            if DIGIT_2[row][col]:
                pattern_cells.add((digit2_start_x + col, start_y + row))

    maze.pattern_cells = pattern_cells

    # Ferme tous les murs des cellules du pattern
    for (cell_x, cell_y) in pattern_cells:
        maze.get_cell(cell_x, cell_y).walls = 0xF

    # Ferme les murs autour du pattern
    for (cell_x, cell_y) in pattern_cells:
        for offset_x, offset_y, wall, _ in DIRECTIONS:
            neighbor_x = cell_x + offset_x
            neighbor_y = cell_y + offset_y
            if 0 <= neighbor_x < maze.width and 0 <= neighbor_y < maze.height:
                if (neighbor_x, neighbor_y) not in pattern_cells:
                    maze.get_cell(neighbor_x, neighbor_y).walls \
                                                            |= OPPOSITE[wall]
