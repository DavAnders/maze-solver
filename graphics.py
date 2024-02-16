from tkinter import Tk, BOTH, Canvas

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
        canvas.pack() #not sure why needing to pack in this method

class Window:
    def __init__(self, width, height):
        self.root_widget = Tk()
        self.root_widget.title("My Application")
        self.canvas = Canvas(self.root_widget, width=width, height=height)
        self.canvas.pack()
        self.is_running = False

        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()
    
    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()
    
    def close(self):
        self.is_running = False
        # self.root_widget.destroy() # might not need this line / leaving for now
    
    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)