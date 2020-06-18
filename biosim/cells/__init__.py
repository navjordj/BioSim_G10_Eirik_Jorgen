__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'

from .dessert import Desert
from .highland import Highland
from .lowland import Lowland
from .water import Water
from .cell import Cell


__all__ = ['Desert', 'Highland', 'Lowland', 'Water', 'Cell']  # For the linter
