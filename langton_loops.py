from grid import GridCell, GridAutomaton, NeighbourhoodType, Neighbourhood


class LangtonCell(GridCell):

    rules = {
        # Current state + NESW neighbours -> new state
        "00000": 0,
        "00001": 2,
        "00002": 0,
        "00003": 0,
        "00005": 0,
        "00006": 3,
        "00007": 1,
        "00011": 2,
        "00012": 2,
        "00013": 2,
        "00021": 2,
        "00022": 0,
        "00023": 0,
        "00026": 2,
        "00027": 2,
        "00032": 0,
        "00052": 5,
        "00062": 2,
        "00072": 2,
        "00102": 2,
        "00112": 0,
        "00202": 0,
        "00203": 0,
        "00205": 0,
        "00212": 5,
        "00222": 0,
        "00232": 2,
        "00522": 2,
        "01232": 1,
        "01242": 1,
        "01252": 5,
        "01262": 1,
        "01272": 1,
        "01275": 1,
        "01422": 1,
        "01432": 1,
        "01442": 1,
        "01472": 1,
        "01625": 1,
        "01722": 1,
        "01725": 5,
        "01752": 1,
        "01762": 1,
        "01772": 1,
        "02527": 1,
        "10001": 1,
        "10006": 1,
        "10007": 7,
        "10011": 1,
        "10012": 1,
        "10021": 1,
        "10024": 4,
        "10027": 7,
        "10051": 1,
        "10101": 1,
        "10111": 1,
        "10124": 4,
        "10127": 7,
        "10202": 6,
        "10212": 1,
        "10221": 1,
        "10224": 4,
        "10226": 3,
        "10227": 7,
        "10232": 7,
        "10242": 4,
        "10262": 6,
        "10264": 4,
        "10267": 7,
        "10271": 0,
        "10272": 7,
        "10542": 7,
        "11112": 1,
        "11122": 1,
        "11124": 4,
        "11125": 1,
        "11126": 1,
        "11127": 7,
        "11152": 2,
        "11212": 1,
        "11222": 1,
        "11224": 4,
        "11225": 1,
        "11227": 7,
        "11232": 1,
        "11242": 4,
        "11262": 1,
        "11272": 7,
        "11322": 1,
        "12224": 4,
        "12227": 7,
        "12243": 4,
        "12254": 7,
        "12324": 4,
        "12327": 7,
        "12425": 5,
        "12426": 7,
        "12527": 5,
        "20001": 2,
        "20002": 2,
        "20004": 2,
        "20007": 1,
        "20012": 2,
        "20015": 2,
        "20021": 2,
        "20022": 2,
        "20023": 2,
        "20024": 2,
        "20025": 0,
        "20026": 2,
        "20027": 2,
        "20032": 6,
        "20042": 3,
        "20051": 7,
        "20052": 2,
        "20057": 5,
        "20072": 2,
        "20102": 2,
        "20112": 2,
        "20122": 2,
        "20142": 2,
        "20172": 2,
        "20202": 2,
        "20203": 2,
        "20205": 2,
        "20207": 3,
        "20212": 2,
        "20215": 2,
        "20221": 2,
        "20222": 2,
        "20227": 2,
        "20232": 1,
        "20242": 2,
        "20245": 2,
        "20252": 0,
        "20255": 2,
        "20262": 2,
        "20272": 2,
        "20312": 2,
        "20321": 6,
        "20322": 6,
        "20342": 2,
        "20422": 2,
        "20512": 2,
        "20521": 2,
        "20522": 2,
        "20552": 1,
        "20572": 5,
        "20622": 2,
        "20672": 2,
        "20712": 2,
        "20722": 2,
        "20742": 2,
        "20772": 2,
        "21122": 2,
        "21126": 1,
        "21222": 2,
        "21224": 2,
        "21226": 2,
        "21227": 2,
        "21422": 2,
        "21522": 2,
        "21622": 2,
        "21722": 2,
        "22227": 2,
        "22244": 2,
        "22246": 2,
        "22276": 2,
        "22277": 2,
        "30001": 3,
        "30002": 2,
        "30004": 1,
        "30007": 6,
        "30012": 3,
        "30042": 1,
        "30062": 2,
        "30102": 1,
        "30122": 0,
        "30251": 1,
        "40112": 0,
        "40122": 0,
        "40125": 0,
        "40212": 0,
        "40222": 1,
        "40232": 6,
        "40252": 0,
        "40322": 1,
        "50002": 2,
        "50021": 5,
        "50022": 5,
        "50023": 2,
        "50027": 2,
        "50052": 0,
        "50202": 2,
        "50212": 2,
        "50215": 2,
        "50222": 0,
        "50224": 4,
        "50272": 2,
        "51212": 2,
        "51222": 0,
        "51242": 2,
        "51272": 2,
        "60001": 1,
        "60002": 1,
        "60212": 0,
        "61212": 5,
        "61213": 1,
        "61222": 5,
        "70007": 7,
        "70112": 0,
        "70122": 0,
        "70125": 0,
        "70212": 0,
        "70222": 1,
        "70225": 1,
        "70232": 1,
        "70252": 5,
        "70272": 0,
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
        return LangtonCell(new_state)

    def activate(self):
        return LangtonCell((self.state + 1) % 8)

    @property
    def color(self):
        return self.state_color_map[self.state]
    

class LangtonLoops(GridAutomaton):

    def __init__(self, **kwargs):
        super().__init__(LangtonCell, Neighbourhood(NeighbourhoodType.VON_NEUMANN, 1, True), frame_rate=25, **kwargs)

    def setup(self):
        super().setup()

        center_x = self.cols // 2
        center_y = self.rows // 2

        start_pattern = [
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
            [2, 1, 7, 0, 1, 4, 0, 1, 4, 2, 0, 0, 0, 0, 0],
            [2, 0, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0, 0],
            [2, 7, 2, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0],
            [2, 1, 2, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0],
            [2, 0, 2, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0],
            [2, 7, 2, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0],
            [2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 0],
            [2, 0, 7, 1, 0, 7, 1, 0, 7, 1, 1, 1, 1, 1, 2],
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
        ]

        offset_x = center_x - len(start_pattern) // 2
        offset_y = center_y - len(start_pattern) // 2

        for y, row in enumerate(start_pattern):
            for x, cell in enumerate(row):
                self.grid[offset_x + x][offset_y + y] = LangtonCell(cell)


if __name__ == "__main__":
    LangtonLoops(rows=88, cols=88, width=880, height=880, gif_path="sim/langton_loops.gif", gif_length=600)
