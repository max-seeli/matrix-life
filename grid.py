from __future__ import annotations
from enum import Enum

from drawing import Container

class GridCell:
    """
    A cell in a grid-based automaton.
    """
    def update(self, neighbours) -> GridCell:
        raise NotImplementedError

    def activate(self) -> GridCell:
        raise NotImplementedError

    @property
    def color(self):
        raise NotImplementedError
    
    @property
    def text(self):
        return None
    

class NeighbourhoodType(Enum):
    """
    A neighbourhood type for grid-based automata.
    """
    MOORE = 1
    VON_NEUMANN = 2


class Neighbourhood:
    """
    A neighbourhood for grid-based automata.
    """
    def __init__(self, type: NeighbourhoodType, radius: int = 1, positional: bool = False):
        self.type = type
        self.radius = radius
        self.positional = positional

    def get_neighbours(self, grid, i, j):
        if self.type == NeighbourhoodType.MOORE:
            return self.__get_moore_neighbours(grid, i, j)
        elif self.type == NeighbourhoodType.VON_NEUMANN:
            return self.__get_von_neumann_neighbours(grid, i, j)

    def __get_moore_neighbours(self, grid, i, j):
        neighbours = []
        for x in range(-self.radius, self.radius + 1):
            for y in range(-self.radius, self.radius + 1):
                if x == 0 and y == 0:
                    continue
                col = (i + x + len(grid)) % len(grid)
                row = (j + y + len(grid[0])) % len(grid[0])
                if self.positional:
                    neighbours.append((grid[col][row], (x, y)))
                else:
                    neighbours.append(grid[col][row])
        return neighbours

    def __get_von_neumann_neighbours(self, grid, i, j):
        neighbours = []
        for x in range(-self.radius, self.radius + 1):
            for y in range(-self.radius, self.radius + 1):
                if abs(x) + abs(y) > self.radius:
                    continue
                if x == 0 and y == 0:
                    continue
                col = (i + x + len(grid)) % len(grid)
                row = (j + y + len(grid[0])) % len(grid[0])
                if self.positional:
                    neighbours.append((grid[col][row], (x, y)))
                else:
                    neighbours.append(grid[col][row])
        return neighbours


class GridAutomaton(Container):
    """
    A grid-based automaton.
    """
    def __init__(self, 
                 cell_type: GridCell,
                 neighbourhood: Neighbourhood = Neighbourhood(NeighbourhoodType.MOORE),
                 rows: int = 20,
                 cols: int = 20,
                 width: int = 500,
                 height: int = 500,
                 frame_rate: int = 5):
        self.cell_type = cell_type
        self.get_neighbours = neighbourhood.get_neighbours
        self.rows = rows
        self.cols = cols
        self.cell_size = int(min(height / self.rows, width / self.cols))
        
        self.running = True
        super().__init__(width, height, frame_rate)
        
    def setup(self):
        self.grid = self.empty_grid()
        
        self.bind("<space>", lambda _: setattr(self, 'running', not self.running))
        
        def get_cell(event):
            bound = lambda value, min_value, max_value: min(max(value, min_value), max_value)

            i = bound(int(event.x / self.cell_size), 0, self.cols - 1)
            j = bound(int(event.y / self.cell_size), 0, self.rows - 1)
            return i, j
        self.bind("<Button-1>", lambda event: self.left_click(*get_cell(event)))
        self.bind("<B1-Motion>", lambda event: self.drag(*get_cell(event)))
        self.bind("<Button-3>", lambda event: self.right_click(*get_cell(event)))

    def draw(self):
        for i in range(self.cols):
            for j in range(self.rows):
                c = self.grid[i][j].color
                t = self.grid[i][j].text
                self.canvas.create_rectangle(
                    i * self.cell_size,
                    j * self.cell_size,
                    (i + 1) * self.cell_size,
                    (j + 1) * self.cell_size,
                    fill=c,
                )
                if t:
                    self.canvas.create_text(
                        i * self.cell_size + self.cell_size / 2,
                        j * self.cell_size + self.cell_size / 2,
                        text=t,
                        fill="#FFFFFF",
                    )
        self.draw_grid(self.cols, self.rows, self.cell_size, color="#2F2F2F")
        
        if self.running:
            self.update()

    def update(self):
        new_grid = self.empty_grid()
        for i in range(self.cols):
            for j in range(self.rows):
                new_grid[i][j] = self.grid[i][j].update(self.get_neighbours(self.grid, i, j))
        self.grid = new_grid

    def left_click(self, i, j):
        self.grid[i][j] = self.grid[i][j].activate()

    def drag(self, i, j):
        self.grid[i][j] = self.grid[i][j].activate()

    def right_click(self, i, j):
        self.grid = self.empty_grid()

    def empty_grid(self):
        return [[self.cell_type()] * self.rows for _ in range(self.cols)]
