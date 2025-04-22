import unittest

from graphics import Maze


class Helper:
    @staticmethod
    def wall_amount(cell):
        return (
            int(cell.has_left_wall)
            + int(cell.has_top_wall)
            + int(cell.has_right_wall)
            + int(cell.has_bottom_wall)
        )

    @staticmethod
    def get_entrance(maze):
        return maze._cells[0][0]

    @staticmethod
    def get_exit(maze):
        return maze._cells[maze.num_cols - 1][maze.num_rows - 1]


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

        num_cols = 0
        num_rows = 0
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m2._cells),
            num_cols,
        )

        num_cols = -5
        num_rows = -9
        m3 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m3._cells),
            0,
        )

    def test_maze_reset_visited(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        for i in range(num_cols):
            for j in range(num_rows):
                cell = m1._cells[i][j]
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()
