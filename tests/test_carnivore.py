__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.animals.carnivore import Carnivore

#@pytest.mark.skip(reason="Not implemented yet")
def test_init_carnivore():
    c = Carnivore(age=2, weight=10)
    assert c.weight == 10
    assert c.age == 2

    # Negative age should raise valuerror 
    with pytest.raises(ValueError) as error:
        print(error)
        c = Carnivore(age=-1, weight=10)

    # Negative weight should raise valuerror 
    with pytest.raises(ValueError) as error:
        print(error)
        c = Carnivore(age=2, weight=-10)

# TODO Nødvendig å teste subclassene?
def test_aging():
    a = Carnivore(age=4, weight=10)
    a.increase_age()
    assert a.age == 5