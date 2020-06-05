__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import random
from math import exp
from typing import Union, Dict
import numpy as np

np.random.seed(1)


def fitness_calc(phi_age: float, a: float, a_half: float, phi_weight: float, w: float, w_half: float) -> float:

    def q(x: float, x_half: float, phi: float, sign: int) -> float:
        return 1 / (1 + exp(sign * phi*(x - x_half)))

    return q(a, a_half, phi_age, 1) * q(w, w_half, phi_weight, -1)


class Animal:
    def __init__(self, age=None, weight=None):  # TODO Fix standard weight value

        self.params: dict = {
            "w_birth": 8.0,
            "sigma_birth": 1.5,
            "beta": 0.9,
            "eta": 0.05,
            "a_half": 40.0,
            "phi_age": 0.6,
            "weight_half": 10.0,
            "phi_weight": 0.1,
            "mu": 0.25,
            "gamma": 0.2,
            "zeta": 3.5,
            "xi": 1.2,
            "omega": 0.4,
            "F": 10.0,
            "delta_phi_max": None
        }
        if age == None:
            self.age: int = 0
        else:
            self.age: int = age
        if weight == None:
            self.weight: float = self.initialize_weight()
        else:
            self.weight: float = weight

        self.fitness = self.get_fitness()
        self.alive = True  # Might not be necessary

    def __str__(self) -> str:
        return f'Type: {type(self)} \n Age: {self.age} \n Fitness: {self.get_fitness()}'

    # TODO implement set_params
    def set_params(self, parameter: Dict[str, Union[int, float]]) -> None:
        raise NotImplementedError("set_params is not implemented yet")

    # TODO: Return value? Bool to confirm success?
    def increase_age(self) -> None:
        self.age += 1

    def death(self) -> bool:
        """
        Returns a boolean saying if the animal should die or not
        """
        if self.fitness <= 0:
            return True
        else:
            p: float = self.params["omega"] * (1-self.fitness)
            return random.random() < p

    # TODO update correct type
    def give_birth(self, N: int) -> Union[object, int]:
        # What is phi?
        p: float = min(1, self.params["gamma"]*self.params["phi_age"]*(N-1))
        if random.random() < p:
            return type(self)()
        else:
            return 0

    def eat(self, intake: Union[int, float]) -> None:
        """ 
        Takes in a certain amount of fodder. Weight change is beta * intake
        """
        fodder_eaten: float = self.params["beta"] * intake
        self.update_weight(fodder_eaten)

    # TODO: Return value? Bool to confirm success?

    def update_weight(self, change: float) -> None:
        self.weight += change
        self.fitness = self.get_fitness()

    # TODO: Return value? Bool to confirm success?

    def new_year(self) -> None:
        """
        Increase age by one year and decrease weight by eta * weight
        """
        self.age += 1
        weight_change: float = -self.params["eta"] * self.weight
        self.update_weight(weight_change)
        self.fitness = self.get_fitness()

    def get_fitness(self) -> float:
        """
        Returns the current fitness of a animal
        """
        if self.weight < 0:
            return 0
        else:
            self.fitness = fitness_calc(self.params["phi_age"], self.age, self.params["a_half"],
                                         self.params["phi_weight"], self.weight, self.params["weight_half"])

        return self.fitness

    def initialize_weight(self) -> float:
        """
        Initializes the weight using a normal distribution
        """
        return np.random.normal(self.params["w_birth"], self.params["sigma_birth"])

    def move(self) -> bool:
        prob = self.params["mu"] * self.fitness
        return np.random.rand() < prob

class Herbivore(Animal):

    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)
        self.params: dict = {
            "w_birth": 8.0,
            "sigma_birth": 1.5,
            "beta": 0.9,
            "eta": 0.05,
            "a_half": 40.0,
            "phi_age": 0.6,
            "weight_half": 10.0,
            "phi_weight": 0.1,
            "mu": 0.25,
            "gamma": 0.2,
            "zeta": 3.5,
            "xi": 1.2,
            "omega": 0.4,
            "F": 10.0,
            "delta_phi_max": None
        }

    @classmethod
    def set_params(cls, params: dict) -> None:
        cls.params = params


class Carnivore(Animal):

    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)
        self.params: dict = {
            "w_birth": 6.0,
            "sigma_birth": 1.0,
            "beta": 0.75,
            "eta": 0.125,
            "a_half": 40.0,
            "phi_age": 0.3,
            "weight_half": 4.0,
            "phi_weight": 0.4,
            "mu": 0.4,
            "gamma": 0.8,
            "zeta": 3.5,
            "xi": 1.1,
            "omega": 0.8,
            "F": 50.0,
            "delta_phi_max": 10
        }

    @classmethod
    def set_params(cls, params: dict) -> None:
        cls.params = params


if __name__ == "__main__":
    h = Herbivore()
    c = Carnivore()
