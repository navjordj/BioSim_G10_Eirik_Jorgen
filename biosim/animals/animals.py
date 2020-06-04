__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import random
from math import exp

def fitness_calc(phi_age, a, a_half, phi_weight, w, w_half):

    def q(x, x_half, phi, sign): 
            return 1/ (1 + exp(sign * phi*(x - x_half)))
    
    return q(a, a_half, phi_age, 1) * q(w, w_half, phi_weight, -1) 

    

class Animal:

    def __init__(self, age, weight):
        if age < 0:
            raise ValueError("Age must be positive")
        else:
            self._age = age
        
        if weight <= 0:
            raise ValueError("Weight must be positive")
        else:
            self._weight = weight
        

    def increase_age(self):
        self.age += 1
        return True

    def death(self):
        pass

    def give_birth(self, gamma: float, phi: float, N: float) -> None: # TODO update correct type
        p = min(1, gamma*phi*(N-1))
        if random.random() < p:
            return type(self)(0, 3)

    
    def update_weight(self, change: float) -> None:
        self.weight += change


    def new_year(self) -> None:
        self._age += 1

    @property
    def get_fitness(self):
        if self._weight < 0:
            return 0
        else:
            self._fitness = None # fitness_calc()
        
        return self._fitness


    @property
    def age(self):
        return self._age

    @property
    def weight(self):
        return self._weight


if __name__ == "__main__":
    a = Animal(10, 3)
    print(a.weight)
    print(a.age)
    print(a.give_birth(1, 2, 4))

    print(fitness_calc(1, 2, 3, 4, 5, 6))

