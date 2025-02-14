
__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'


import pytest
import numpy as np
import scipy.stats as stats
from pytest_mock import mocker

from biosim.animals.animal import Animal


def test_init_animal_and_weight():
    # Checks that the weight is close to a normal distribution
    alpha = 0.001
    n = 10000
    a = Animal()
    # makes a normal distribution from the parameters w_birth and sigma_birth
    norm_disp = np.random.normal(a.params["w_birth"], a.params["sigma_birth"], n)
    # list with weights of animals when not any specified weight is given
    weight_list = []
    for _ in range(n):
        a = Animal()
        weight_list.append(a.weight)
    # compares the weight_list against the normal distribution, the closer they are, the bigger the
    # p-value gets
    x = np.concatenate((weight_list, norm_disp))
    k2, p = stats.normaltest(x)
    assert p >= alpha

    assert a.age == 0
    a: Animal = Animal(age=2, weight=10)
    assert a.age == 2
    assert a.weight == 10


def test_set_params():
    a: Animal = Animal()

    a.set_params({"F": 25.0})
    assert a.params["F"] == 25.0

    with pytest.raises(ValueError) as error:
        invalid_params = {"F": -50}
        a.set_params(invalid_params)

    with pytest.raises(ValueError) as error:
        invalid_params = {"not_a_param": 100}
        a.set_params(invalid_params)


def test_aging():
    a: Animal = Animal()
    a.increase_age()
    assert a.age == 1

    a.age = 5
    assert a.age == 5


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
    prob_death, infected = a.should_die()
    assert prob_death is True and infected is False

    mocker.patch('numpy.random.random', return_value=1)

    a = Animal()
    prob_death, infected = a.should_die()
    assert prob_death is False

    a = Animal()
    a.infected = True
    prob_death, infected = a.should_die()
    assert prob_death is False and infected is True
    # probability of death is close to a normal distribution
    alpha = 0.00001
    n = 1000
    death_list = []  # list of prob of death for animal
    for _ in range(n):
        a = Animal()
        death_list.append(a.params["omega"] * (1 - a.fitness))
    # Central limit theorem
    mean = np.mean(death_list)
    std = np.std(death_list)
    assert n * mean >= 30 and n * (1 - mean) >= 30  # test for close to normal
    norm_approx = np.random.normal(mean, std, n)  # makes a normal distribution from mean and std
    x = np.concatenate((death_list, norm_approx))
    k2, p = stats.normaltest(x)
    assert p > alpha


def test_birth(mocker):
    a = Animal()
    N = 1000
    assert a.give_birth(N) is False

    N = 0
    assert a.give_birth(N) is False

    a.has_migrated = True
    assert a.give_birth(N) is False

    mocker.patch('random.random', return_value=0)
    b = Animal(weight=40)
    assert b.give_birth(100) is True

    c = Animal(weight=40)
    assert c.give_birth(0) is False


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
    # Tests that fitness is close to normal when a newborn is placed in the simulation
    alpha = 0.00001
    n = 1000
    fitness_list = []
    for _ in range(n):
        a = Animal()
        fitness_list.append(a.get_fitness())
    fitness_list2 = []
    for _ in range(n):
        a = Animal()
        fitness_list.append(a.get_fitness())
    # Central limit theorem
    mean = np.mean(fitness_list)
    sd = np.std(fitness_list)
    assert n * mean >= 10 and n * (1 - mean) >= 10  # test if close to normal
    norm_approx = np.random.normal(mean, sd, n)
    x = np.concatenate((fitness_list2, norm_approx))
    k2, p = stats.normaltest(x)
    assert p > alpha

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

    # Test that negative weight always gives fitness of zero
    a: Animal = Animal()
    a.weight = -1
    assert a.get_fitness() == 0


def test_will_migrate():
    # fitness ~ 1
    # mu = 0.25
    # Probability should be 0.25 (mu*fitness)

    n_migrations = 0
    for _ in range(10000):
        a: Animal = Animal(age=1, weight=10000)
        assert a.has_migrated is False
        if a.will_migrate():
            n_migrations += 1
            assert a.has_migrated is True
            assert a.will_migrate() is False  # Animal will not migrate once has_migrated = True

    prob_migration = n_migrations/10000
    assert prob_migration == pytest.approx(0.25, abs=1e-2)
