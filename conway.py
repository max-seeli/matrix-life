from grid import GridCell, GridAutomaton


class ConwayCell(GridCell):
    
    def __init__(self, alive=False):
        self.alive = alive

    def update(self, neighbours):
        count = sum(n.alive for n in neighbours)
        if not self.alive and count == 3:
            return ConwayCell(True)
        elif self.alive and (count < 2 or count > 3):
            return ConwayCell(False)
        else:
            return ConwayCell(self.alive)

    def activate(self):
        return ConwayCell(True)
        
    @property
    def color(self):
        return "black" if self.alive else "white"


class GameOfLife(GridAutomaton):
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
        def __init__(self, **kwargs):
            super().__init__(ConwayCell, **kwargs)

if __name__ == "__main__":
    GameOfLife()
