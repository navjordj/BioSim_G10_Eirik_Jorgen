__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.cell import Cell, Water, Lowland, Highland, Desert
from biosim.animals import Animal, Herbivore, Carnivore


def test_cell() -> None:
    Cell()


def test_change_params() -> None:
    k = Cell()
    with pytest.raises(ValueError):
        k.set_parameters(fodder=-1)
    k.set_parameters(fodder=300)
    assert k.fodder == 300


#  is this the right way to check migration?
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


#  is this function necessary ?
def test_migration() -> None:
    """
    Does the same as in last test, but now it uses the function instead of
    """
    w = Water()
    l = Lowland()
    h = Highland()
    d = Desert()
    assert w.migrate() is False
    assert l.migrate() is True
    assert h.migrate() is True
    assert d.migrate() is True


# TODO try to make it not look too ugly
def test_eat_herbivore() -> None:
    """
    Tests if an animal that eats gains weight
    and tests if there is no food the weight is the same
    """
    l = Lowland()
    l.add_animal(Herbivore())
    start_weight_lowland = 0.0  # mypy refused to take in anything other than a float (see animals)
    for herb in l.herbivores:
        start_weight_lowland += herb.weight
    fodder_before_eating_lowland = l.fodder
    l.eat_herbivore()
    fodder_end_of_eating_lowland = l.fodder
    new_weight_lowland = 0.0
    for herb in l.herbivores:
        new_weight_lowland += herb.weight
    assert new_weight_lowland >= start_weight_lowland  # see if weight has increased
    assert fodder_before_eating_lowland >= fodder_end_of_eating_lowland  # see if the amount of
    # fodder is lower after eating

    d = Desert()
    d.add_animal(Herbivore())
    fodder_before_eating_desert = d.fodder
    start_weight_desert = 0.0
    for herb in d.herbivores:
        start_weight_desert += herb.weight
    d.eat_herbivore()
    fodder_end_of_eating_desert = d.fodder
    new_weight_desert = 0.0
    for herb in d.herbivores:
        new_weight_desert += herb.weight
    assert new_weight_desert == start_weight_desert
    assert fodder_before_eating_desert == 0
    assert fodder_before_eating_desert == fodder_end_of_eating_desert


def test_add_animal() -> None:
    c = Cell()
    h = Herbivore()
    a = Animal()
    c.add_animal(h)
    assert len(c.herbivores) == 1
    assert c.herbivores[0] == h
    with pytest.raises(ValueError):
        c.add_animal(a)


def test_dead_herbivore():
    """
    Tests if the herbivore list gets shorter when one dies
    """
    l = Lowland()
    n = 5
    for _ in range(n):
        l.add_animal(Herbivore())
    for herb in l.herbivores:
        assert herb.alive is True
    assert l.n_herbivores == n
    l.herbivores[0].alive = False
    l.remove_dead_herbivore()
    assert l.n_herbivores == n-1


# TODO find a way to test eat_carnivore function, have to implement more
def test_eat_carnivore():
    """
    Sees if 10 carnivores gain any weight after trying to eat 10 herbivores
    """
    d = Desert()
    n = 10
    for _ in range(n):
        d.add_animal(Herbivore())
    for _ in range(n):
        d.add_animal(Carnivore())
    start_weight_carnivore = 0.0
    for carn in d.carnivores:
        start_weight_carnivore += carn.weight
    d.eat_carnivore()
    end_weight_carnivore = 0.0
    for carn in d.carnivores:
        end_weight_carnivore += carn.weight
    assert start_weight_carnivore < end_weight_carnivore


# TODO test new year
def test_new_year_function():
    l = Lowland()
    l.add_animal(Herbivore())
    pass



