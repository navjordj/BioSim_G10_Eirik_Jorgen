__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.animals.herbivore import Herbivore

# @pytest.mark.skip(reason="Not implemented yet")
def test_init_herbivore():
    h: Herbivore = Herbivore(age=2, weight=10)
    assert h.weight == 10
    assert h.age == 2

    with pytest.raises(ValueError) as error:
        print(error)
        h: Herbivore = Herbivore(age=-1, weight=10)

    with pytest.raises(ValueError) as error:
        print(error)
        h: Herbivore = Herbivore(age=2, weight=-10)


def test_aging():
    h: Herbivore = Herbivore(age=4, weight=10)
    h.increase_age()
    assert h.age == 5

def test_weight():
    h: Herbivore = Herbivore(age=4, weight=10)
    h.update_weight(10)
    assert h.weight == 20

    h: Herbivore = Herbivore(age=4, weight=10)
    h.update_weight(-5)
    assert h.weight == 5

def test_fitness():

    # Check that fitness decreases when age increases
    a: Herbivore = Herbivore(age=2, weight=10)
    fit_before: float = a.get_fitness()
    a.increase_age()
    fit_after: float = a.get_fitness()
    assert fit_after < fit_before

    # Check that fitness increases when weight increases
    a: Herbivore = Herbivore(age=2, weight=10)
    fit_before: float = a.get_fitness()
    a.update_weight(10)
    fit_after: float = a.get_fitness()
    assert fit_after > fit_before

    # Test that the fitness goes towards 0 when aging
    a: Herbivore = Herbivore(age=2, weight=10)
    for _ in range(1000):
        a.increase_age()
    assert a.get_fitness() == pytest.approx(0)

    # Test that fitness goes towards 1 as weight increases
    a: Herbivore = Herbivore(age=2, weight=10)
    a.update_weight(10000)
    assert a.get_fitness() == pytest.approx(1)

