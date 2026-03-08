import random
from mlx import Mlx  # type: ignore
from src.maze import Maze, NORTH, SOUTH, EAST, WEST
from src.color import ColorManager  # type: ignore

CELL_SIZE = 20
WALL_SIZE = 3
MAZE_MARGIN = 15     # écart entre la fenêtre et le maze
BUTTON_W = 80        # largeur d'un bouton
BUTTON_H = 28        # hauteur d'un bouton
BUTTON_GAP = 15      # écart entre les boutons
BUTTON_MARGIN = 15   # écart entre le maze et les boutons


class Display:

    def __init__(self, width: int, height: int, maze_params=None,
                 generate_maze_func=None, buttons=None) -> None:
        self.maze_height = height
        self.width = width + 2 * MAZE_MARGIN
        self.height = (height + 2 * MAZE_MARGIN + BUTTON_MARGIN +
                       BUTTON_H + BUTTON_MARGIN)
        self.buttons = buttons or []
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(self.mlx_ptr, self.width,
                                           self.height, "A-Maze-ing")
        self.maze = None
        self.img = self.mlx.mlx_new_image(self.mlx_ptr, self.width,
                                          self.height)
        self.pythondata, self.bpp, self.sl, _ = \
            self.mlx.mlx_get_data_addr(self.img)
        self.maze_params = maze_params
        self.generate_maze_func = generate_maze_func
        self.need_redraw = True
        self.color_manager = ColorManager()

    def clear_image(self) -> None:
        black = (0xFF000000).to_bytes(4, 'little') * (len(self.pythondata)
                                                      // 4)
        self.pythondata[:] = black

    def _put_pixel(self, px: int, py: int, color: bytes) -> None:
        offset = (py * self.sl) + (px * (self.bpp // 8))
        if offset + 4 <= len(self.pythondata):
            self.pythondata[offset:offset + 4] = color

    def draw_horizontal_wall(self, x: int, y: int, y_offset: int) -> None:
        row = (y + y_offset) * CELL_SIZE + MAZE_MARGIN
        color = self.color_manager.current()
        for t in range(WALL_SIZE):
            for px in range(x * CELL_SIZE + MAZE_MARGIN,
                            (x + 1) * CELL_SIZE + MAZE_MARGIN):
                self._put_pixel(px, row + t, color)

    def draw_vertical_wall(self, x: int, y: int, x_offset: int) -> None:
        col = (x + x_offset) * CELL_SIZE + MAZE_MARGIN
        color = self.color_manager.current()
        for t in range(WALL_SIZE):
            for py in range(y * CELL_SIZE + MAZE_MARGIN,
                            (y + 1) * CELL_SIZE + MAZE_MARGIN):
                self._put_pixel(col + t, py, color)

    def set_maze(self, maze: Maze) -> None:
        self.maze = maze

    def _fill_interior(self, x: int, y: int, color: bytes) -> None:
        x_start = x * CELL_SIZE + MAZE_MARGIN + WALL_SIZE
        y_start = y * CELL_SIZE + MAZE_MARGIN + WALL_SIZE
        x_end = (x + 1) * CELL_SIZE + MAZE_MARGIN
        y_end = (y + 1) * CELL_SIZE + MAZE_MARGIN
        for py in range(y_start, y_end):
            for px in range(x_start, x_end):
                self._put_pixel(px, py, color)

    def draw_cell(self, x: int, y: int) -> None:
        cell = self.maze.get_cell(x, y)
        if (x, y) in self.maze.pattern_cells:
            b, g, r, a = self.color_manager.current()
            interior = bytes([b // 4, g // 4, r // 4, a])
            self._fill_interior(x, y, interior)
        if cell.has_wall(NORTH):
            self.draw_horizontal_wall(x, y, 0)
        if cell.has_wall(SOUTH):
            self.draw_horizontal_wall(x, y, 1)
        if cell.has_wall(WEST):
            self.draw_vertical_wall(x, y, 0)
        if cell.has_wall(EAST):
            self.draw_vertical_wall(x, y, 1)

    def _button_rects(self):
        n = len(self.buttons)
        total_w = n * BUTTON_W + (n - 1) * BUTTON_GAP
        x0 = (self.width - total_w) // 2 - 30
        y0 = self.maze_height + MAZE_MARGIN + BUTTON_MARGIN
        return [(x0 + i * (BUTTON_W + BUTTON_GAP), y0, BUTTON_W, BUTTON_H)
                for i in range(n)]

    def draw_button_labels(self) -> None:
        if not self.buttons:
            return
        for (bx, by, bw, bh), btn in zip(self._button_rects(), self.buttons):
            self.mlx.mlx_string_put(self.mlx_ptr, self.win,
                                    bx + 8, by + bh // 2 - 5,
                                    0xFFFFFFFF, btn["label"])

    def cycle_color(self) -> None:
        self.color_manager.cycle()
        self.need_redraw = True

    def regenerate(self) -> None:
        if not (self.maze_params and self.generate_maze_func):
            return
        params = self.maze_params
        maze = Maze(params['WIDTH'], params['HEIGHT'],
                    params['ENTRY'], params['EXIT'])
        self.generate_maze_func(maze, seed=random.randint(0, 2**31),
                                perfect=params.get('PERFECT', True))
        self.set_maze(maze)
        self.need_redraw = True

    def close_window(self, key, param) -> None:
        if key == 65307:   # Échap
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        elif key == 114:   # R
            self.regenerate()
        elif key == 99:    # C
            self.cycle_color()

    def render(self, param) -> None:
        if self.need_redraw:
            self.clear_image()
            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    self.draw_cell(x, y)
            self.need_redraw = False
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win,
                                         self.img, 0, 0)
        self.draw_button_labels()

    def draw_maze(self) -> None:
        if self.maze is None:
            print("Error: Maze not set for display.")
            return
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render, None)
        self.mlx.mlx_key_hook(self.win, self.close_window, None)
        self.mlx.mlx_mouse_hide(self.mlx_ptr)
        self.mlx.mlx_loop(self.mlx_ptr)
