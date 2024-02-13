import colorsys
from drawing import Container

class FloatingConway(Container):
    """
    A version of Conway's Game of Life with a floating point grid. For easier
    understanding, the grid is visualized with colors. The current state of a
    cell will subsequently be called the "activation" of the cell and is a
    floating point number between 0 and 1.

    Controls:
    - Left click to draw cells (click and drag to draw multiple cells)
    - Right click to clear the grid
    - Middle click to take one step in the simulation
    - Space to pause/resume the simulation

    Rules:
    - Any cell with cumulative neighbour activation less than 2 or greater than
      3 will decrease its activation by 15%. (Compare to overpopulation and
      underpopulation in the original Game of Life)
    - Any cell with cumulative neighbour activation equal to 3 +/- 0.15 will 
      set its activation to 1. (Compare to reproduction in the original Game
      of Life)
    - All other cells will remain at their current activation.
    """
        
    def setup(self):
        self.cols = 80
        self.rows = 80
        self.cell_size = min(self.height / self.rows, self.width / self.cols)

        self.grid = [[0] * self.rows for _ in range(self.cols)]           
        self.running = True

        self.bind("<Button-1>", self.activate)
        self.bind("<B1-Motion>", self.activate)
        self.bind("<Button-3>", self.clear)
        self.bind("<Button-2>", self.update)
        self.bind("<space>", self.pause)

    def draw(self):
        for i in range(self.cols):
            for j in range(self.rows):
                c = self.float_to_color(self.grid[i][j])
                self.canvas.create_rectangle(
                    i * self.cell_size,
                    j * self.cell_size,
                    (i + 1) * self.cell_size,
                    (j + 1) * self.cell_size,
                    fill=c,
                )
        self.draw_grid(self.cols, self.rows, self.cell_size, color="#2F2F2F")
        
        if self.running:
            self.update()

    def float_to_color(self, state, start_hue=230, end_hue=320):
        state = max(0, min(1, state))

        hue = start_hue + (end_hue - start_hue) * state
        saturation = 1.0
        value = 0.8

        r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
    
    def update(self, _=None):
        new_grid = [[0] * self.rows for _ in range(self.cols)]
        for i in range(self.cols):
            for j in range(self.rows):
                neighbours = self.get_neighbourhood_activation(i, j)

                if (neighbours < 2 or neighbours > 3):
                    new_grid[i][j] = self.grid[i][j] * 0.85
                elif abs(neighbours - 3) < 0.15:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = self.grid[i][j]

        self.grid = new_grid

    def get_neighbourhood_activation(self, x, y):
        total_activation = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                col = (x + i + self.cols) % self.cols
                row = (y + j + self.rows) % self.rows
                
                total_activation += self.grid[col][row]
    
        total_activation -= self.grid[x][y]
        return total_activation
    
    def draw_pattern(self, x, y):
        pattern = [
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
        ]
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                self.grid[(x + i) % self.cols][(y + j) % self.rows] = pattern[i][j]

    def activate(self, event):
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


FloatingConway(800, 800)
