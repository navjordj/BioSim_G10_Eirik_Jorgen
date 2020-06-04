__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import random
from math import exp
from typing import Union
import numpy as np

 
def fitness_calc(phi_age: float, a: float, a_half: float, phi_weight: float, w: float, w_half: float) -> float:

    def q(x: float, x_half: float, phi: float, sign: int) -> float:
        return 1 / (1 + exp(sign * phi*(x - x_half)))

    return q(a, a_half, phi_age, 1) * q(w, w_half, phi_weight, -1)


params = {
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


class Animal:
    # TODO remove age. Age is always 0 at birth
    def __init__(self, age=0, weight=0): # TODO Fix standard weight value

        self._params: dict = params

        if age < 0:
            raise ValueError("Age must be positive")
        else:
            self._age: float = age

        if weight <= 0:
            raise ValueError("Weight must be positive")
        else:
            self._weight: float = self.initialize_weight()

        self._fitness = self.get_fitness()
        self.alive = True # Might not be necessary


    def __str__(self):
        return f'Type: {type(self)} \n Age: {self._age} \n Fitness: {self.get_fitness()}'

    def increase_age(self):
        self._age += 1
        return True

    def death(self):
        pass
    
    # TODO update correct type
    def give_birth(self, gamma: float, phi: float, N: float) -> Union[object, int]:
        p = min(1, gamma*phi*(N-1))
        if random.random() < p:
            return type(self)(0, 3)
        else:
            return 0

    def eat(self, intake: Union[int, float]):
        """ 
        Takes in a certain amount of fodder. Weight change is beta * intake
        """
        fodder_eaten: float = self._params["beta"] * intake
        self.update_weight(fodder_eaten)



    def update_weight(self, change: float) -> None:
        self._weight += change
    

    def new_year(self) -> None:
        """
        Increase age by one year and decrease weight by eta * weight
        """
        self._age += 1
        weight_change: float = -self._params["eta"] * self._weight
        self.update_weight(weight_change)
        self._fitness = self.get_fitness()
 

    def get_fitness(self) -> Union[int, float]:
        """
        Returns the current fitness of a animal
        """
        if self._weight < 0:
            return 0
        else:
            self._fitness = fitness_calc(self._params["phi_age"], self._age, self._params["a_half"],
                                         self._params["phi_weight"], self._weight, self._params["weight_half"])

        return self._fitness

    def initialize_weight(self) -> float:
        """
        Initializes the weight using a normal distribution
        """
        return np.random.normal(self._params["w_birth"], self._params["sigma_birth"])

    def move(self) -> bool:
        prob = self._params["mu"] * self._fitness
        return np.random.random < prob

    @property
    def age(self):
        return self._age

    @property
    def weight(self):
        return self._weight


if __name__ == "__main__":
    a = Animal(10, 3)
    a.new_year()
    print(a)

