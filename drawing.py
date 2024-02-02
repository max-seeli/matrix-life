from tkinter import *

class Container:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.root = Tk()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.setup()
        self.root.after(0, self.draw)
        self.root.mainloop()

    def setup(self):
        pass

    def draw(self):
        pass

    def bind(self, event, callback):
        self.root.bind(event, callback)

    def draw_grid(self, cols, rows, cell_size, color="light gray", linewidth=1):
        for i in range(cols + 1):
            self.canvas.create_line(i * cell_size, 0,
                                    i * cell_size, rows * cell_size,
                                    fill=color, width=linewidth)
        for j in range(rows + 1):
            self.canvas.create_line(0, j * cell_size,
                                    cols * cell_size, j * cell_size,
                                    fill=color, width=linewidth)
