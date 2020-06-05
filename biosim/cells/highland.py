__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


from biosim.cells.cell import Cell


class Highland(Cell):

    max_fodder = 300

    def __init__(self) -> None:
        super().__init__()
        self.fodder = self.max_fodder

    def grow(self) -> None:
        self.fodder = self.max_fodder
