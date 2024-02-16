import time
from cell import Cell
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._cells = []

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
        
    
    def _knock_down_wall(self, i, j, ni, nj):
        if i < ni: # moving down
            self._cells[i][j].has_bottom_wall = False
            self._cells[ni][nj].has_top_wall = False
        elif i > ni: # moving up
            self._cells[i][j].has_top_wall = False
            self._cells[ni][nj].has_bottom_wall = False
        elif j < nj: # moving right
            self._cells[i][j].has_right_wall = False
            self._cells[ni][nj].has_left_wall = False
        elif j > nj: # moving left
            self._cells[i][j].has_left_wall = False
            self._cells[ni][nj].has_right_wall = False
        #might need to redraw cells

    
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        directions = [('up', 0, -1), ('right', 1, 0), ('down', 0, 1), ('left', -1, 0)]
        while True:
            possible_moves = []
            for direction, di, dj, in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < self._num_rows and 0 <= nj < self._num_cols and not self._cells[ni][nj].visited:
                    possible_moves.append((ni, nj))
            if not possible_moves:
                self._draw_cell(i, j)
                return
            ni, nj = random.choice(possible_moves)
            self._knock_down_wall(i, j, ni, nj)
            self._break_walls_r(ni, nj)
        
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        bottom_row_index = self._num_rows - 1
        bottom_col_index = self._num_cols - 1
        self._cells[bottom_row_index][bottom_col_index].has_bottom_wall = False
        self._draw_cell(bottom_row_index, bottom_col_index)


    def _create_cells(self):
        for i in range(self._num_rows):  # Iterate over rows
            row_cells = []
            for j in range(self._num_cols):  # Iterate over columns within each row
                cell = Cell(self._win)
                row_cells.append(cell)
            self._cells.append(row_cells)


    def _draw_cell(self, i, j):
        x1 = self._x1 + j * self._cell_size_x
        y1 = self._y1 + i * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        cell = self._cells[i][j]
        cell.set_coordinates(x1, y1, x2, y2)
        cell.draw()
        self._animate()
    
    def _animate(self):
        if self._win is not None:
            self._win.redraw()
            time.sleep(0.05)
    
    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()

        # Mark the current cell as visited
        self._cells[i][j].visited = True

        # If we are at the end cell, we are done
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        movements = {
            'left': (0, -1, 'has_left_wall'),
            'right': (0, 1, 'has_right_wall'),
            'up': (-1, 0, 'has_top_wall'),
            'down': (1, 0, 'has_bottom_wall')
        }

        # Try each possible movement
        for direction, (di, dj, wall_attr) in movements.items():
            ni, nj = i + di, j + dj
            if 0 <= ni < self._num_rows and 0 <= nj < self._num_cols:
                # Check if there is no wall blocking the way to the new cell
                # and it hasn't been visited
                if not getattr(self._cells[i][j], wall_attr) and not self._cells[ni][nj].visited:
                    # Draw a move to the new cell
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    
                    # Recursively attempt to solve from the new cell
                    if self._solve_r(ni, nj):
                        return True  # Found end
                        
                    # If moving to new cell didn't solve the maze, undo move
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)

        # None of the directions worked out
        return False