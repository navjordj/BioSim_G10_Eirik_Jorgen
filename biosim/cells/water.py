from biosim.cells.cell import Cell


class Water(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.allowed_move_to = False
