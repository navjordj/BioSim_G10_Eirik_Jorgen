__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'

from .cell import Cell


class Desert(Cell):
    """
    Subclass of the superclass Cell
    """

    def __init__(self) -> None:
        super().__init__()
