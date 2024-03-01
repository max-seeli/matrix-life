from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from drawing import Container

class GridCell(ABC):
    """
    A cell in a grid-based automaton.
    """
    @abstractmethod
    def update(self, neighbours) -> GridCell:
        raise NotImplementedError

    @abstractmethod
    def activate(self) -> GridCell:
        raise NotImplementedError

    @property
    @abstractmethod
    def color(self):
        raise NotImplementedError
    

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
    def __init__(self, type: NeighbourhoodType, radius: int = 1):
        self.type = type
        self.radius = radius

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
        super().__init__(width, height, frame_rate)
        
    def setup(self):
        self.cell_size = int(min(self.height / self.rows, self.width / self.cols))
        self.grid = self.__init_grid()
        
        self.running = True
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

    def update(self):
        new_grid = self.__init_grid()
        for i in range(self.cols):
            for j in range(self.rows):
                new_grid[i][j] = self.grid[i][j].update(self.get_neighbours(self.grid, i, j))
        self.grid = new_grid

    def left_click(self, i, j):
        self.grid[i][j] = self.grid[i][j].activate()

    def drag(self, i, j):
        self.grid[i][j] = self.grid[i][j].activate()

    def right_click(self, i, j):
        self.grid = self.__init_grid()

    def __init_grid(self):
        return [[self.cell_type()] * self.rows for _ in range(self.cols)]
