__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.cells import Highland


def test_highland() -> None:
    """
        Checks tht the fodder has been updated
        from 0 too a new number just by starting the function

        Checks if allowed_move_to is the default boll (True)
        """
    h = Highland()
    assert h.fodder != 0
    assert h.allowed_move_to is True
