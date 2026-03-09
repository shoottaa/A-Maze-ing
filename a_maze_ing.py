import sys
from src.parse_config import parse_config
from src.generate import generate_maze
from src.maze import Maze
from src.solve import write_output
from src.display import Display, CELL_SIZE


def main() -> None:
    """Fonction principale"""
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py <input_file>")
        sys.exit(1)

    config = parse_config(sys.argv[1])

    maze = Maze(config["WIDTH"], config["HEIGHT"],
                config["ENTRY"], config["EXIT"])
    generate_maze(maze, perfect=config["PERFECT"])

    write_output(maze, config["OUTPUT_FILE"])

    maze_params = {
        'WIDTH': config["WIDTH"],
        'HEIGHT': config["HEIGHT"],
        'ENTRY': config["ENTRY"],
        'EXIT': config["EXIT"],
        'PERFECT': config["PERFECT"],
    }

    buttons = [
        {"label": "R: Regen;",   "action": None},
        {"label": "P: Path;", "action": None},
        {"label": "C: Color;", "action": None},
        {"label": "ESC: Exit;", "action": None},
    ]

    display = Display(config["WIDTH"] * CELL_SIZE,
                      config["HEIGHT"] * CELL_SIZE,
                      maze_params=maze_params,
                      generate_maze_func=generate_maze,
                      buttons=buttons)

    buttons[0]["action"] = display.regenerate
    buttons[2]["action"] = display.cycle_color
    display.set_maze(maze)
    display.draw_enter(config["ENTRY"][0], config["ENTRY"][1])
    display.draw_exit(config["EXIT"][0], config["EXIT"][1])
    display.draw_maze()


if __name__ == "__main__":
    main()
