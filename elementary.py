from drawing import Container
from warnings import warn

class ElementaryCellularAutomaton(Container):
    """
    The simplest class of one-dimensional cellular automata.

    Each cell has a binary state, either 0 or 1. The rules are based on the
    state of the cell and its two neighbors. There are 8 possible states, the
    cell triplet can be in. For each of these states, the rule specifies the
    new state of the cell in the next generation. There are 256 possible rules,
    as each of the 8 states can result in either 0 or 1.

    Controls:
    - Left click to toggle the state of a cell.
    - Right click to clear the grid.
    - Middle click to take a step in the simulation.
    - Space to run/pause the simulation.

    Visualization:
    - The top row is the initial state of the grid.
    - At each step, the next row is calculated based on the previous row.

    Source: https://en.wikipedia.org/wiki/Elementary_cellular_automaton
    """
    def __init__(self, width=810, height=600, cols=81, rule=22, start_pattern=[1], **kwargs):
        self.cols = cols
        self.cell_size = width // self.cols
        self.rows = height // self.cell_size
            
        self.rule = rule
        
        if len(start_pattern) > self.cols:
            warn(f"Start pattern is too long, only the first {self.cols} cells will be used.")
            self.start_pattern = start_pattern[:self.cols]
        else:
            self.start_pattern = start_pattern

        self.running = True 

        super().__init__(width, height, **kwargs)

    def setup(self):
        self.state = [0] * self.cols

        start_offset = (self.cols - len(self.start_pattern)) // 2
        self.state[start_offset:start_offset + len(self.start_pattern)] = self.start_pattern

        self.history = [self.state] 

        self.ruleset = [int(bit) for bit in bin(self.rule)[2:].zfill(8)]

        self.bind("<Button-1>", self.on_click)
        self.bind("<Button-3>", self.clear)
        self.bind("<Button-2>", self.step)
        self.bind("<space>", self.pause)      

    def draw(self):
        self.draw_grid(self.cols, self.rows, self.cell_size)
        for j, state in enumerate(self.history):
            for i, cell in enumerate(state):
                if cell == 1:
                    self.canvas.create_rectangle(
                        i * self.cell_size,
                        j * self.cell_size,
                        (i + 1) * self.cell_size,
                        (j + 1) * self.cell_size,
                        fill="black",
                    )
        if self.running:
            self.step()
    
    def step(self, _=None):
        next_state = [0] * self.cols
        for i in range(0, self.cols):
            neighbours = self.get_neighbours(i)
            next_state[i] = self.ruleset[7 - int("".join(map(str, neighbours)), 2)]
        self.history.append(next_state)
        self.state = next_state
        if len(self.history) > self.rows:
            self.history.pop(0)

    def get_neighbours(self, x):
        return [self.state[(x + i + self.cols) % self.cols] for i in [-1, 0, 1]]
    
    def on_click(self, event):
        x = event.x // self.cell_size
        x = min(max(x, 0), self.cols - 1)

        self.state[x] = 1 - self.state[x]
        self.history = [self.state]

    def clear(self, _):
        self.state = [0] * self.cols
        self.history = [self.state]

    def pause(self, _):
        self.running = not self.running


ElementaryCellularAutomaton(gif_path="sim/elementary_rule22.gif", gif_length=150)
