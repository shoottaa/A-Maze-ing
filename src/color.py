WALL_COLORS = [
    0xFFFFFFFF,  # blanc (défaut)
    0xFFFF0000,  # rouge
    0xFF00FF00,  # vert
    0xFF0000FF,  # bleu
    0xFFFFFF00,  # jaune
    0xFF00FFFF,  # cyan
    0xFFFF00FF,  # magenta
]


class ColorManager:

    def __init__(self) -> None:
        self.index = 0

    def current(self) -> bytes:
        return WALL_COLORS[self.index].to_bytes(4, 'little')

    def cycle(self) -> None:
        self.index = (self.index + 1) % len(WALL_COLORS)
