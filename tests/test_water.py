__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.water import Water


def test_water() -> None:
    w = Water()
    assert w.fodder == 0
    assert w.allowed_move_to is False
