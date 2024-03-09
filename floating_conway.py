import colorsys
from grid import GridCell, GridAutomaton, NeighbourhoodType, Neighbourhood

class FloatingConwayCell(GridCell):
    
    def __init__(self, activation=0):
        self.activation = activation

    def update(self, neighbours):
        total_activation = sum(n.activation for n in neighbours)
        if (total_activation < 2 or total_activation > 3):
            return FloatingConwayCell(self.activation * 0.85)
        elif abs(total_activation - 3) < 0.15:
            return FloatingConwayCell(1)
        else:
            return FloatingConwayCell(self.activation)

    def activate(self):
        return FloatingConwayCell(1)

    @property
    def color(self):
        return self.float_to_color(self.activation)

    def float_to_color(self, state, start_hue=230, end_hue=320):
        state = max(0, min(1, state))

        hue = start_hue + (end_hue - start_hue) * state
        saturation = 1.0
        value = 0.8

        r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'
    

class FloatingConway(GridAutomaton):
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
    def __init__(self, pattern, **kwargs):
        self.pattern = pattern
        super().__init__(FloatingConwayCell, **kwargs)

    def setup(self):
        super().setup()

        center_x = self.cols // 2
        center_y = self.rows // 2
        offset_x = center_x - len(self.pattern) // 2
        offset_y = center_y - len(self.pattern) // 2
        for y, row in enumerate(self.pattern):
            for x, cell in enumerate(row):
                self.grid[offset_x + x][offset_y + y] = FloatingConwayCell(cell)

    pattern1 = [
            [0, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 1, 0, 0],
    ]

if __name__ == "__main__":
    conway = FloatingConway(pattern=FloatingConway.pattern1, rows=30, cols=30, width=600, height=600, gif_path="sim/floating_conway.gif", gif_length=275)
    
