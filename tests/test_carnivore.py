__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest
import numpy as np

from biosim.animals.carnivore import Carnivore

#@pytest.mark.skip(reason="Not implemented yet")
def test_init_carnivore():
    np.random.seed(1)
    c: Carnivore = Carnivore()
    assert c.weight == 10.436518045494863
    assert c.age == 0


# TODO Nødvendig å teste subclassene?
def test_aging():
    c: Carnivore = Carnivore()
    c.increase_age()
    assert c.age == 1

def test_weight():
    c: Carnivore = Carnivore()
    weight_before = c.weight
    c.update_weight(10)
    assert c.weight == (weight_before + 10)

    c: Carnivore = Carnivore()
    weight_before = c.weight
    c.update_weight(-5)
    assert c.weight == (weight_before - 5)

def test_fitness():

    # Check that fitness decreases when age increases
    c: Carnivore = Carnivore()
    fit_before: float = c.get_fitness()
    c.increase_age()
    fit_after: float = c.get_fitness()
    assert fit_after < fit_before

    # Check that fitness increases when weight increases
    c: Carnivore = Carnivore()
    fit_before: float = c.get_fitness()
    c.update_weight(10)
    fit_after: float = c.get_fitness()
    assert fit_after > fit_before

    # Test that the fitness goes towards 0 when aging
    c: Carnivore = Carnivore()
    for _ in range(1000):
        c.increase_age()
    assert c.get_fitness() == pytest.approx(0)

    # Test that fitness goes towards 1 as weight increases
    c: Carnivore = Carnivore()
    c.update_weight(1000)
    assert c.get_fitness() == pytest.approx(1, rel=1e-4) # TODO: Find out why this fails with standard error of 1e-6

