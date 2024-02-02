from drawing import Container

class GameOfLife(Container):
    """
    Conway's Game of Life
    
    Controls:
    - Left click to draw cells (click and drag to draw multiple cells)
    - Right click to clear the grid
    - Middle click or space to pause the simulation

    Rules:
    - Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    - Any live cell with two or three live neighbours lives on to the next generation.
    - Any live cell with more than three live neighbours dies, as if by overpopulation.
    - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

    Source: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    """
        
    def setup(self):
        self.cols = 80
        self.rows = 60
        self.cell_size = min(self.height / self.rows, self.width / self.cols)

        self.grid = [[0] * self.rows for _ in range(self.cols)]
        self.running = True

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Button-3>", self.clear)
        self.bind("<Button-2>", self.pause)
        self.bind("<space>", self.pause)

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid(self.cols, self.rows, self.cell_size)
        for i in range(self.cols):
            for j in range(self.rows):
                if self.grid[i][j] == 1:
                    self.canvas.create_rectangle(
                        i * self.cell_size,
                        j * self.cell_size,
                        (i + 1) * self.cell_size,
                        (j + 1) * self.cell_size,
                        fill="black",
                    )
        if self.running:
            self.update()
        self.root.after(100, self.draw)
    
    def get_neighbours(self, x, y):
        neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                neighbours += self.grid[col][row]
        neighbours -= self.grid[x][y]
        return neighbours
    
    def update(self):
        new_grid = [[0] * self.rows for _ in range(self.cols)]
        for i in range(self.cols):
            for j in range(self.rows):
                state = self.grid[i][j]
                neighbours = self.get_neighbours(i, j)
                if state == 0 and neighbours == 3:
                    new_grid[i][j] = 1
                elif state == 1 and (neighbours < 2 or neighbours > 3):
                    new_grid[i][j] = 0
                else:
                    new_grid[i][j] = state
        self.grid = new_grid

    def on_click(self, event):
        x, y = self.get_cell(event)
        self.grid[x][y] = 1 - self.grid[x][y]

    def on_drag(self, event):
        x, y = self.get_cell(event)
        self.grid[x][y] = 1

    def get_cell(self, event):
        bound = lambda value, min_value, max_value: min(max(value, min_value), max_value)

        x = bound(int(event.x / self.cell_size), 0, self.cols - 1)
        y = bound(int(event.y / self.cell_size), 0, self.rows - 1)
        return x, y

    def clear(self, _):
        self.grid = [[0] * self.rows for _ in range(self.cols)]

    def pause(self, _):
        self.running = not self.running


GameOfLife(800, 600)