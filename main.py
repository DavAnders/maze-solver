from graphics import Line, Point, Window
from cell import Cell
from maze import Maze
import random

def draw_maze(self):
    for row in self.maze._cells:
        for cell in row:
            cell.draw()

def main():
    win = Window(800, 600)
    
    seed = 42
    random.seed(seed)
    
    maze = Maze(0, 0, 10, 10, 40, 40, win, seed)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()