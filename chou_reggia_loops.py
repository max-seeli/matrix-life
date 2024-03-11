from grid import GridCell, GridAutomaton, NeighbourhoodType, Neighbourhood


class ChouReggiaCell(GridCell):

    rules = {
        # Current state + NESW neighbours -> new state
        "00000": 0,  
        "00044": 0,
        "00054": 7,
        "00010": 0,
        "00011": 0,
        "00033": 0,
        "00404": 0,
        "00444": 5,
        "00410": 0,
        "00104": 0,
        "00101": 0,
        "00174": 0,
        "00300": 0,
        "00301": 0,
        "00303": 0,
        "00704": 0,
        "00703": 0,
        "00710": 4,
        "00711": 0,
        "04000": 0,
        "04007": 0,
        "04710": 0,
        "05000": 7,
        "01700": 0,
        "07000": 0,
        "07007": 7,
        "07101": 0,
        "40010": 1,
        "40031": 3,
        "40103": 3,
        "40710": 3,
        "41103": 3,
        "43103": 3,
        "50003": 3,
        "50333": 0,
        "10004": 5,
        "10001": 1,
        "10041": 4,
        "10104": 4,
        "10130": 1,
        "10301": 1,
        "10713": 1,
        "14041": 4,
        "14104": 4,
        "11104": 4,
        "13301": 1,
        "17771": 1,
        "30401": 1,
        "30501": 1,
        "30514": 1,
        "30714": 1,
        "34401": 1,
        "34501": 1,
        "35401": 0,
        "31400": 1,
        "37771": 1,
        "70000": 0,
        "70033": 7,
        "70710": 0,
        "70714": 1,
        "70711": 0,
        "71700": 0,
        "73000": 7,
        "77007": 0,
        "77071": 1,
    }
    coord_pos_map = {
        (0, -1): "up",
        (1, 0): "right",
        (0, 1): "down",
        (-1, 0): "left",
    }
    state_color_map = {
        0: "black",
        1: "blue",
        2: "red",
        3: "green",
        4: "yellow",
        5: "magenta",
        6: "white",
        7: "cyan",
    }

    def __init__(self, state=0):
        self.state = state

    def update(self, neighbours):
        pos_neighbours = {}
        for n, (x, y) in neighbours:
            pos_neighbours[self.coord_pos_map[(x, y)]] = n.state

        # Convert coordinates and states to a string representing the neighbourhood
        neighbours_state = ''.join(
            str(pos_neighbours[dir]) for dir in
            ["up", "right", "down", "left"]
        )

        # Generate all rotations of the neighbourhood
        all_rotations = [neighbours_state[i:] + neighbours_state[:i] for i in range(4)]

        # Find the new state based on the rules
        new_state = next(
            (self.rules[f"{self.state}{rotation}"] for rotation in all_rotations if f"{self.state}{rotation}" in self.rules),
            self.state  # Default to current state if no rule matches
        )
        return ChouReggiaCell(new_state)

    def activate(self):
        return ChouReggiaCell((self.state + 1) % 8)

    @property
    def color(self):
        return self.state_color_map[self.state]
    

class ChouReggiaLoops(GridAutomaton):

    def __init__(self, **kwargs):
        super().__init__(ChouReggiaCell, Neighbourhood(NeighbourhoodType.VON_NEUMANN, 1, True), frame_rate=25, **kwargs)

    def setup(self):
        super().setup()

        center_x = self.cols // 2
        center_y = self.rows // 2

        start_pattern = [
            [1, 1, 0],
            [3, 4, 1],
        ]

        offset_x = center_x - len(start_pattern) // 2
        offset_y = center_y - len(start_pattern) // 2

        for y, row in enumerate(start_pattern):
            for x, cell in enumerate(row):
                self.grid[offset_x + x][offset_y + y] = ChouReggiaCell(cell)


if __name__ == "__main__":
    ChouReggiaLoops(rows=88, cols=88, width=880, height=880, gif_path="sim/chou_reggia_loops.gif", gif_length=200)
