
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest
import numpy as np

from biosim.animals.animals import Animal


# @pytest.mark.skip(reason="Not implemented yet")
def test_init_animal():
    np.random.seed(1)

    a: Animal = Animal()
    print(a.weight)
    assert a.age == 0
    assert a.weight == 10.436518045494863


def test_aging():
    a: Animal = Animal()
    a.increase_age()
    assert a.age == 1

def test_weight():
    a: Animal = Animal()
    weight_before = a.weight
    a.update_weight(10)
    assert a.weight == weight_before+10

    a: Animal = Animal()
    weight_before = a.weight
    a.update_weight(-5)
    assert a.weight == weight_before - 5

def test_fitness():

    # Check that fitness decreases when age increases
    a: Animal = Animal()
    fit_before: float = a.get_fitness()
    a.increase_age()
    fit_after: float = a.get_fitness()
    assert fit_after < fit_before

    # Check that fitness increases when weight increases
    a: Animal = Animal()
    fit_before: float = a.get_fitness()
    a.update_weight(10)
    fit_after: float = a.get_fitness()
    assert fit_after > fit_before

    # Test that the fitness goes towards 0 when aging
    a: Animal = Animal()
    for _ in range(1000):
        a.increase_age()
    assert a.get_fitness() == pytest.approx(0)

    # Test that fitness goes towards 1 as weight increases
    a: Animal = Animal()
    a.update_weight(10000)
    assert a.get_fitness() == pytest.approx(1)



    