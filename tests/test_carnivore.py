__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'


import pytest
import numpy as np
import scipy.stats as stats


from biosim.animals import Carnivore, Herbivore

def test_init_carnivore():
    alpha = 0.001
    n = 10000
    a = Carnivore()
    norm_disp = np.random.normal(a.params["w_birth"], a.params["sigma_birth"], n)
    weight_list = []
    for _ in range(n):
        a = Carnivore()
        weight_list.append(a.weight)
    x = np.concatenate((weight_list, norm_disp))
    k2, p = stats.normaltest(x)
    if p >= alpha:
        assert True
    else:
        assert False
    assert a.age == 0

    a: Carnivore = Carnivore(age=2, weight=10)
    assert a.age == 2
    assert a.weight == 10


def test_eat_carnivore() -> None:
    c = Carnivore()
    h = Herbivore()
    c.set_params({'DeltaPhiMax': 0})
    c.p_eat(c.get_fitness(), h.get_fitness(), c.params['DeltaPhiMax'])


