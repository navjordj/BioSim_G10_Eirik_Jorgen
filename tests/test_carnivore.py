__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.animals.carnivore import Carnivore

#@pytest.mark.skip(reason="Not implemented yet")
def test_carnivore():
    c = Carnivore(2, 10)
    assert c.weight == 10
    assert c.age == 2

    with pytest.raises(ValueError) as error:
        print(error)
        c = Carnivore(-1, 10)

    with pytest.raises(ValueError) as error:
        print(error)
        c = Carnivore(2, -10)