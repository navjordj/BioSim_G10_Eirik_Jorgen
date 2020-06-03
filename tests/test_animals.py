
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.animals.animals import Animal

# @pytest.mark.skip(reason="Not implemented yet")
def test_animal():
    a = Animal(age=2, weight=10)
    assert a.age == 2
    assert a.weight == 10


    with pytest.raises(ValueError) as error:
        print(error)
        a = Animal(age=-1, weight=10)

    with pytest.raises(ValueError) as error:
        print(error)
        a = Animal(age=2, weight=-10)
