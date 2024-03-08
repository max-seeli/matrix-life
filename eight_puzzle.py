from grid import GridAutomaton, GridCell
from warnings import warn
from random import choice

class EightPuzzleCell(GridCell):
    """
    A cell for the 8-puzzle game.
    """
    def __init__(self, value):
        self.value = value

    @property
    def color(self):
        if self.value == 0:
            return "#ffffff"
        else:
            return "#174a9c"
        
    @property
    def text(self):
        if self.value == 0:
            return ""
        else:
            return str(self.value)
        

class EightPuzzle(GridAutomaton):

    def __init__(self, **kwargs):
        super().__init__(EightPuzzleCell, rows=3, cols=3, frame_rate=1, **kwargs)

    def setup(self):

        self.grid = [
            [EightPuzzleCell(1), EightPuzzleCell(2), EightPuzzleCell(3)],
            [EightPuzzleCell(4), EightPuzzleCell(5), EightPuzzleCell(6)],
            [EightPuzzleCell(7), EightPuzzleCell(0), EightPuzzleCell(8)],
        ]
        self.grid = list(map(list, zip(*self.grid)))

        self.shuffle()

        self.solver = EightPuzzleSolver(self)
        self.solver.solve()
        self.move_idx = 0

    def update(self):
        if self.solver.solution:
            if self.move_idx < len(self.solver):
                move = self.solver[self.move_idx]
                self.grid = EightPuzzleSolver.apply_move(self.grid, move)
                self.move_idx += 1
        else:
            warn("No solution found")

    def shuffle(self, iterations=1000):

        for _ in range(iterations):
            possible_moves = EightPuzzleSolver.get_possible_moves(self.grid)
            
            move = choice(possible_moves)
            self.grid = EightPuzzleSolver.apply_move(self.grid, move)


    
                

class EightPuzzleSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.reset()

    def reset(self):
        self.queue = [([], self.puzzle.grid)]
        self.visited = set()
        self.solution = None

    def solve(self):
        while self.queue:
            path, grid = self.queue.pop(0)
            if self.is_solved(grid):
                self.solution = path
                return
            self.visited.add(self.grid_to_string(grid))
            for move in self.get_possible_moves(grid):
                new_grid = self.apply_move(grid, move)
                if self.grid_to_string(new_grid) not in self.visited:
                    self.queue.append((path + [move], new_grid))

    def is_solved(self, grid):
        return self.grid_to_string(grid) == "123456780"


    @staticmethod
    def apply_move(grid, move):
        x, y = EightPuzzleSolver.get_empty_position(grid)
        new_x, new_y = x + move[0], y + move[1]
        new_grid = [row[:] for row in grid]
        
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_grid[x][y], new_grid[new_x][new_y] = new_grid[new_x][new_y], new_grid[x][y]
        else:
            warn("Invalid move")
        
        return new_grid    

    @staticmethod
    def get_possible_moves(grid):
        x, y = EightPuzzleSolver.get_empty_position(grid)
        moves = []
        if x > 0:
            moves.append((-1, 0))
        if x < 2:
            moves.append((1, 0))
        if y > 0:
            moves.append((0, -1))
        if y < 2:
            moves.append((0, 1))
        return moves
    
    @staticmethod
    def get_empty_position(grid):
        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                if cell.value == 0:
                    return x, y

    def grid_to_string(self, grid):
        rep = ""
        for x, row in enumerate(grid):
            for y, cell in enumerate(row):
                rep += str(grid[y][x].value)
        return rep


    def __len__(self):
        return len(self.solution)

    def __getitem__(self, index):
        return self.solution[index]
    
if __name__ == "__main__":
    EightPuzzle()