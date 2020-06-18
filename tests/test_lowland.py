__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'


import pytest

from biosim.cells import Lowland


def test_lowland() -> None:
    """
    Checks tht the fodder has been updated
    from 0 too a new number just by starting the function

    Checks if allowed_move_to is the default boll (True)
    """
    l = Lowland()
    assert l.fodder != 0
    assert l.allowed_move_to is True
