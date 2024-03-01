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
    def __init__(self, **kwargs):
        super().__init__(FloatingConwayCell, **kwargs)

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

if __name__ == "__main__":
    FloatingConway()
    
