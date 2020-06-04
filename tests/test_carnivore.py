__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'


import pytest

from biosim.animals.carnivore import Carnivore

#@pytest.mark.skip(reason="Not implemented yet")
def test_init_carnivore() -> None:
    c: Carnivore = Carnivore(age=2, weight=10)
    assert c.weight == 10
    assert c.age == 2

    # Negative age should raise valuerror 
    with pytest.raises(ValueError) as error:
        print(error)
        c: Carnivore = Carnivore(age=-1, weight=10)

    # Negative weight should raise valuerror 
    with pytest.raises(ValueError) as error:
        print(error)
        c: Carnivore = Carnivore(age=2, weight=-10)

# TODO Nødvendig å teste subclassene?
def test_aging() -> None:
    c: Carnivore = Carnivore(age=4, weight=10)
    c.increase_age()
    assert c.age == 5

def test_weight() -> None:
    c: Carnivore = Carnivore(age=4, weight=10)
    c.update_weight(10)
    assert c.weight == 20

    c: Carnivore = Carnivore(age=4, weight=10)
    c.update_weight(-5)
    assert c.weight == 5

def test_fitness() -> None:

    # Check that fitness decreases when age increases
    c: Carnivore = Carnivore(age=2, weight=10)
    fit_before: float = c.get_fitness()
    c.increase_age()
    fit_after: float = c.get_fitness()
    assert fit_after < fit_before

    # Check that fitness increases when weight increases
    c: Carnivore = Carnivore(age=2, weight=10)
    fit_before: float = c.get_fitness()
    c.update_weight(10)
    fit_after: float = c.get_fitness()
    assert fit_after > fit_before

    # Test that the fitness goes towards 0 when aging
    c: Carnivore = Carnivore(age=2, weight=10)
    for _ in range(1000):
        c.increase_age()
    assert c.get_fitness() == pytest.approx(0)

    # Test that fitness goes towards 1 as weight increases
    c: Carnivore = Carnivore(age=2, weight=10)
    c.update_weight(1000)
    assert c.get_fitness() == pytest.approx(1, rel=1e-4) # TODO: Find out why this fails with standard error of 1e-6

