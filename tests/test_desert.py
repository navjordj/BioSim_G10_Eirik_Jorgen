__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.cells.desert import Desert


def test_desert() -> None:
    d = Desert()
    assert d.fodder == 0
    assert d.allowed_move_to is True
