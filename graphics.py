import random
from time import sleep
from tkinter import BOTH, Canvas, Tk


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Generator")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True

        while self.__running:
            self.redraw()

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def close(self):
        self.__running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.x = Point(x1, y1)
        self.y = Point(x2, y2)
        self._win = win

    def draw(self):
        if not self._win:
            return

        line = Line(Point(self.x.x, self.y.x), Point(self.x.x, self.y.y))
        empty_color = "white"
        if self.has_left_wall:
            self._win.draw_line(line, "red")
        else:
            self._win.draw_line(line, empty_color)

        line = Line(Point(self.x.x, self.y.x), Point(self.x.y, self.y.x))
        if self.has_top_wall:
            self._win.draw_line(line, "blue")
        else:
            self._win.draw_line(line, empty_color)

        line = Line(Point(self.x.y, self.y.x), Point(self.x.y, self.y.y))
        if self.has_right_wall:
            self._win.draw_line(line, "green")
        else:
            self._win.draw_line(line, empty_color)

        line = Line(Point(self.x.x, self.y.y), Point(self.x.y, self.y.y))
        if self.has_bottom_wall:
            self._win.draw_line(line, "yellow")
        else:
            self._win.draw_line(line, empty_color)

    def draw_move(self, to_cell, undo=False):
        if not self._win:
            return

        current_center_cell = Point(
            (self.x.x + self.y.x) / 2, (self.x.y + self.y.y) / 2
        )
        target_center_cell = Point(
            (to_cell.x.x + to_cell.y.x) / 2, (to_cell.x.y + to_cell.y.y) / 2
        )

        line = Line(current_center_cell, target_center_cell)
        fill_color = "gray" if undo else "red"

        line.draw(self._win.canvas, fill_color=fill_color)


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, seed=None, win=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        # self._break_entrance_and_exit()
        # self._break_walls_r(0, 0)
        # self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []

            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size_x
                y1 = self._y1 + j * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y

                cell = Cell(x1, y1, x2, y2, self._win)
                col_cells.append(cell)
                self._draw_cell(cell)
            self._cells.append(col_cells)

    def _draw_cell(self, cell):
        cell.draw()
        self._animate()

    def _animate(self):
        if not self._win:
            return

        self._win.redraw()
        sleep(0.01)

    def _break_entrance_and_exit(self):
        if not self._cells:
            return
        entrance = self._cells[0][0]
        exit = self._cells[-1][-1]

        entrance.has_top_wall = False
        entrance.draw()

        exit.has_bottom_wall = False
        exit.draw()

    def _break_walls_r(self, i, j):
        if not self._cells:
            return
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))

            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))

            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))

            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self._draw_cell(self._cells[i][j])
                return

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        if not self._cells:
            return

        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        if not self._cells:
            return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()

        # vist the current cell
        self._cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_cols - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_rows - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False
