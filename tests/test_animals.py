
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest
import numpy as np
import scipy.stats as stats
from pytest_mock import mocker

from biosim.animals import Animal


def test_init_animal():
    alpha = 0.001
    n = 10000
    a = Animal()
    norm_disp = np.random.normal(a.params["w_birth"], a.params["sigma_birth"], n)
    weight_list = []
    for _ in range(n):
        a = Animal()
        weight_list.append(a.weight)
    x = np.concatenate((weight_list, norm_disp))
    k2, p = stats.normaltest(x)
    if p >= alpha:
        assert True
    else:
        assert False
    assert a.age == 0

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


def test_death(mocker):
    a = Animal()
    a.weight = 0
    assert a.should_die() is True
    
    mocker.patch('random.random', return_value=1)
    a = Animal()
    assert a.should_die() is False


def test_birth(mocker):
    a = Animal()
    N = 1000
    assert a.give_birth(N) is False

    N = 0
    assert a.give_birth(N) is False

    mocker.patch('random.random', return_value=-10000)
    b = Animal(weight=40)
    assert b.give_birth(100) is True


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

# TODO confidence interval
def test_fitness():
    alpha = 0.05
    n = 1000
    fitness_list = []
    for _ in range(n):
        a = Animal()
        fitness_list.append(a.get_fitness())

    mean = np.median(np.array(fitness_list))

    df = n - 1
    expected_value = mean
    standard_error = (expected_value*(1-expected_value)/n)**0.5
    sd = stats.t.std(df)
    critical_value = stats.t.ppf((1+alpha)/2, df)
    norm_fitness = 0
    for fitness in fitness_list:
        diff = abs(expected_value - fitness)
        t_score = diff/sd
        p = stats.t.cdf(t_score, df=df)*2
        print(p, critical_value)
        if p > 1-alpha:
            norm_fitness += 1
    print(norm_fitness)
    assert n-(n*alpha) < norm_fitness
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
    a.update_weight(1000000) # TODO see if I can make it "right"
    #assert a.get_fitness() == pytest.approx(1)
