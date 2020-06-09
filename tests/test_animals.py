
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest
import numpy as np
import scipy.stats as stats

from biosim.animals import Animal


# @pytest.mark.skip(reason="Not implemented yet")
def test_init_animal():
    alpha = 0.05
    n = 10000
    prob_list = []
    for _ in range(n):
        a: Animal = Animal()
        z = (a.weight - a.params["w_birth"])/a.params["sigma_birth"]
        prob = stats.norm.sf(z)
        if prob > alpha:
            prob_list.append(prob)
    assert a.age == 0
    assert len(prob_list) > 1-(n*alpha)

    a: Animal = Animal(age=2, weight=10)
    assert a.age == 2
    assert a.weight == 10


def test_aging():
    a: Animal = Animal()
    a.increase_age()
    assert a.age == 1


def test_update_weight():
    a: Animal = Animal()
    weight_before = a.weight
    a.update_weight(10)
    assert a.weight == weight_before+10

    a: Animal = Animal()
    weight_before = a.weight
    a.update_weight(-5)
    assert a.weight == weight_before - 5


# @pytest.mark.skip(reason="Not implemented yet")
def test_death():
    np.random.seed(1)
    a = Animal()
    a.weight = 0
    print(a.fitness)
    assert a.should_die() is True

    a = Animal()
    a.fitness = 1
    assert a.should_die() is False


# @pytest.mark.skip(reason="Not implemented yet")
def test_birth():
    a: Animal = Animal()
    N = 1000
    assert a.give_birth(N) == False

    N = 0
    assert a.give_birth(N) == False

def test_eat():
    a: Animal = Animal()
    
    weight_before = a.weight
    intake = 10
    a.eat(10)
    assert a.weight == (weight_before + a.params["beta"]*intake)

    # Eat negative amount should raise a ValueError
    with pytest.raises(ValueError) as error:
        a: Animal = Animal()
        a.eat(-10)

def test_new_year():
    a: Animal = Animal()

    weight_before = a.weight
    a.new_year()
    assert a.weight == (weight_before - a.params["eta"]*weight_before)

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
    a.update_weight(1000000)
    #assert a.get_fitness() == pytest.approx(1)
