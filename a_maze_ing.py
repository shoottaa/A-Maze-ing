import sys
from src.parse_config import parse_config


def show_menu() -> str:
    print("\n=== A-Maze-ing ===")
    print("1. Re-générer un nouveau labyrinthe")
    print("2. Afficher / Cacher le chemin")
    print("3. Changer la couleur des murs")
    print("4. Quitter")
    return input("Choix (1-4) : ").strip()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python a_maze_ing.py <input_file>")
        sys.exit(1)

    config = parse_config(sys.argv[1])

    while True:
        choice = show_menu()
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            sys.exit(0)
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    main()
