__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import random
from math import exp
from typing import Union, Dict
import numpy as np

np.random.seed(1)


def fitness_calc(a: float, a_half: float, phi_age: float,  w: float, w_half: float, phi_weight: float) -> float:

    def q(x: float, x_half: float, phi: float, sign: int) -> float:
        return 1 / (1 + exp(sign * phi*(x - x_half)))

    return q(a, a_half, phi_age, 1) * q(w, w_half, phi_weight, -1)


class Animal:
    # TODO Possible rewrite to normal attributes (no dict)
    params: dict = {
            "w_birth": 8.0,
            "sigma_birth": 1.5,
            "beta": 0.9,
            "eta": 0.05,
            "a_half": 40.0,
            "phi_age": 0.2,
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
    
    def __init__(self, age=None, weight=None):  # TODO Fix standard weight value
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
        self.has_migrated = False

    def __str__(self) -> str:
        return f'Type: {type(self)} \n Age: {self.age} \n Fitness: {self.get_fitness()}'

    # TODO implement set_params
    @classmethod
    def set_params(cls, new_parameters: Dict[str, Union[int, float]]) -> None:

        for key in new_parameters:
            try:
                if new_parameters[key] >= 0:
                    cls.params[key] = new_parameters[key]
                else:
                    raise ValueError(f'Key for {key} cant be negative ({new_parameters[key]}')
            except ValueError as error:
                print(error)
    # TODO: Return value? Bool to confirm success?
    def increase_age(self) -> None:
        self.age += 1

    def should_die(self) -> bool:
        """
        Returns a boolean saying if the animal should die or not
        """
        if self.weight <= 0:
            return True
        else:
            p: float = self.params["omega"] * (1 - self.fitness)
            return np.random.random() < p

    # TODO update correct type
    def give_birth(self, N: int) -> bool:

        if self.weight < self.params["zeta"] * (self.params["w_birth"] + self.params["sigma_birth"]):
            return False

        p: Union[int, float] = min(1, self.params["gamma"]*self.fitness*(N-1))
        if np.random.random() < p:
            return True
        else:
            return False

    def eat(self, intake: Union[int, float]) -> None:
        """ 
        Takes in a certain amount of fodder. Weight change is beta * intake
        """
        if intake < 0:
            raise ValueError("Cant eat negative amount")
        else:
            weight_change: float = self.params["beta"] * intake
            self.update_weight(weight_change)

    # TODO: Return value? Bool to confirm success?

    def update_weight(self, change: float) -> None:
        self.weight += change
        self.fitness = self.get_fitness()

    # TODO: Return value? Bool to confirm success?

    def new_year(self) -> None:
        """
        Increase age by one year and decrease weight by eta * weight
        """
        self.has_migrated = False
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
            self.fitness = fitness_calc(self.age, self.params["a_half"], self.params["phi_age"], 
                                         self.weight, self.params["weight_half"], self.params["phi_weight"] )

        return self.fitness

    def initialize_weight(self) -> float:
        """
        Initializes the weight using a normal distribution
        """
        return np.random.normal(self.params["w_birth"], self.params["sigma_birth"])

    def will_migrate(self) -> bool:
        prob = self.params["mu"] * self.get_fitness()
        if np.random.rand() < prob:
            self.has_migrated = True
            return True
        else:
            return False


class Herbivore(Animal):
    params: dict = {
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
    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)


class Carnivore(Animal):
    params: dict = {
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

    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)

if __name__ == "__main__":
    h1 = Herbivore()
    h2 = Herbivore()
    print(h2.params)
    h1.set_params({"w_birth": 100})
    print(h2.params)