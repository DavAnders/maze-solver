import unittest
from main import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_break_entrance_and_exit(self):
        maze = Maze(0, 0, 5, 5, 10, 10)  # Adjust parameters as needed
        maze._break_entrance_and_exit()
        self.assertFalse(maze._cells[0][0].has_top_wall, "Entrance wall not removed")
        self.assertFalse(maze._cells[4][4].has_bottom_wall, "Exit wall not removed")
    
    def test_reset_cells_visited(self):
        # Create a Maze instance (adjust parameters as needed)
        maze = Maze(0, 0, 5, 5, 40, 40, None)  # Assuming None for the window parameter
        
        # simulate visiting some cells
        maze._cells[0][0].visited = True
        maze._cells[1][1].visited = True
        
        # Reset visited property of all cells
        maze._reset_cells_visited()
        
        # Check if all cells are marked as not visited
        all_not_visited = all(cell.visited == False for row in maze._cells for cell in row)
        self.assertTrue(all_not_visited, "Not all cells were reset to visited = False")

if __name__ == "__main__":
    unittest.main()
