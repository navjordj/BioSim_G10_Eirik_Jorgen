__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import pytest
from pytest_mock import mocker

from biosim.cell import Cell, Water, Lowland, Highland, Desert
from biosim.animals import Animal, Herbivore, Carnivore

import numpy as np
import random


def test_cell() -> None:
    Cell()
    i = Cell()
    print(i)


def test_change_params() -> None:
    l = Lowland()
    h = Highland()

    with pytest.raises(ValueError):
        l.set_parameters({'f_max': -1})
    with pytest.raises(ValueError):
        h.set_parameters({'f_max': -1})
    l.set_parameters({'f_max': 400})
    h.set_parameters({'f_max': 400})
    l.grow() # Reset fodder in cell to max_fodder
    h.grow()
    assert l.fodder == 400
    assert h.fodder == 400

    c = Lowland()
    with pytest.raises(ValueError):
        c.set_parameters({'f_max': -1})
    c.set_parameters({'f_max': 300})
    c.grow()
    assert c.params['f_max'] == 300

    l = Lowland()
    before = l.fodder
    l.set_parameters({'f_max': 900})
    l.grow()
    print(l.params['f_max'], l.fodder)
    assert l.fodder > before


def test_allowed_to_move_to() -> None:
    """
    Tests the parameter inside every landscape type to see if allowed to move to
    """
    w = Water()
    l = Lowland()
    h = Highland()
    d = Desert()
    assert w.allowed_move_to is False
    assert l.allowed_move_to is True
    assert h.allowed_move_to is True
    assert d.allowed_move_to is True


def test_remove_animal() -> None:
    h = Highland()
    h.add_animal('Herbivore')
    n_before = h.n_herbivores
    h.remove_animal(h.herbivores[0])
    assert n_before > h.n_herbivores

    h.add_animal('Carnivore')
    n_before = h.n_carnivores
    h.remove_animal(h.carnivores[0])
    assert n_before > h.n_carnivores

    a = 'Animal'
    with pytest.raises(ValueError):
        h.remove_animal(a)


# TODO try to make it not look too ugly
def test_eat_herbivore() -> None:
    """
    Tests if an animal that eats gains weight
    and tests if there is no food the weight is the same
    """
    l = Lowland()
    l.add_animal('Herbivore')
    start_weight_lowland = l.herbivores[0].weight
    fodder_before_eating_lowland = l.fodder
    l.eat_herbivore()
    fodder_end_of_eating_lowland = l.fodder
    new_weight_lowland = l.herbivores[0].weight
    assert new_weight_lowland >= start_weight_lowland  # see if weight has increased
    assert fodder_before_eating_lowland >= fodder_end_of_eating_lowland  # see if the amount of
    # fodder is lower after eating
    l.grow()
    assert l.fodder >= fodder_end_of_eating_lowland and l.fodder == l.params['f_max']  # fodder is set
    # to the standard amount of fodder (max fodder)

    d = Desert()
    d.add_animal('Herbivore')
    fodder_before_eating_desert = d.fodder
    start_weight_desert = d.herbivores[0].weight
    d.eat_herbivore()
    fodder_end_of_eating_desert = d.fodder
    new_weight_desert = d.herbivores[0].weight
    assert new_weight_desert == start_weight_desert
    assert fodder_before_eating_desert == 0
    assert fodder_before_eating_desert == fodder_end_of_eating_desert

    h = Highland()
    h.add_animal('Herbivore')
    start_weight_highland = h.herbivores[0].weight
    h.set_parameters({'f_max': 11})
    h.eat_herbivore()
    assert h.herbivores[0].weight > start_weight_highland


def test_add_animal() -> None:
    c = Cell()
    h = 'Herbivore'
    a = 'Animal'
    c.add_animal(h)
    assert len(c.herbivores) == 1
    assert type(c.herbivores[0]) == type(Herbivore())
    with pytest.raises(ValueError):
        c.add_animal(a)


def test_eat_carnivore(mocker) -> None:
    """
    Sees if 10 carnivores gain any weight after trying to eat 10 herbivores
    """
    mocker.patch('random.random', return_value=0) # TODO update to numpy

    d = Desert()
    d.add_animal('Carnivore')
    start_weight_carnivore = d.carnivores[0].weight
    d.eat_carnivore()
    assert start_weight_carnivore == d.carnivores[0].weight
    d.add_animal('Herbivore')
    start_weight_carnivore = d.carnivores[0].weight
    d.eat_carnivore()
    end_weight_carnivore = d.carnivores[0].weight
    assert start_weight_carnivore < end_weight_carnivore
    assert d.herbivores[0].alive is False


def test_remove_dead_animals() -> None:
    l = Lowland()
    n = 5
    for _ in range(n):
        l.add_animal('Carnivore')
        l.add_animal('Herbivore')
    for carn in l.carnivores:
        assert carn.alive is True
    for herb in l.herbivores:
        assert herb.alive is True
    assert l.n_carnivores == n
    assert l.n_herbivores == n
    l.carnivores[0].alive = False
    l.herbivores[0].alive = False
    l.remove_dead_animals()
    assert l.n_carnivores == n - 1 and l.n_herbivores == n - 1


# TODO try to make mock or a statistic method (already done in animals?)
def test_animal_babies() -> None:
    l = Lowland()

    l.animal_babies()
    assert l.n_herbivores == 0
    assert l.n_carnivores == 0
    n = 10
    for _ in range(n):
        l.add_animal('Herbivore', weight=100, age=5)
        l.add_animal('Carnivore', weight=100, age=5)

    num_herb_pre_procreation = l.n_herbivores
    num_carni_pre_procreation = l.n_carnivores
    l.animal_babies()
    assert num_herb_pre_procreation < l.n_herbivores and num_carni_pre_procreation < l.n_carnivores


def test_death_animal() -> None:
    d = Desert()
    n = 100
    for _ in range(n):
        d.add_animal('Carnivore')
        d.add_animal('Herbivore')
    num_carni_pre_prob = d.n_carnivores
    num_herb_pre_prob = d.n_herbivores
    d.death_animals()
    assert num_carni_pre_prob > d.n_carnivores and num_herb_pre_prob > d.n_herbivores


def test_grow() -> None:
    l = Lowland()
    n = 10
    for _ in range(n):
        l.add_animal('Herbivore')
    l.eat_herbivore()
    finished_eating = l.fodder
    l.grow()
    assert l.fodder == l.params['f_max']
    assert l.fodder > finished_eating


def test_new_year():
    l = Lowland()
    l.add_animal('Carnivore')
    l.add_animal('Herbivore')
    age_pre_carn = l.carnivores[0].age
    age_pre_herb = l.herbivores[0].age
    weight_pre_carn = l.carnivores[0].weight
    weight_pre_herb = l.herbivores[0].weight
    l.new_year()
    assert age_pre_carn < l.carnivores[0].age and age_pre_herb < l.herbivores[0].age
    assert weight_pre_carn > l.carnivores[0].weight and weight_pre_herb > l.herbivores[0].weight
