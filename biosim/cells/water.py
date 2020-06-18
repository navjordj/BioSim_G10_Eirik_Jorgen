__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'


from .cell import Cell


class Water(Cell):
    """
    Documentation for desert cell type
    """

    def __init__(self) -> None:
        super().__init__()
        self.allowed_move_to = False
