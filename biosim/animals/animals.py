__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import random

def fitness_calc() -> float:
    pass

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

    
    def update_weight(self, change):
        self.weight += change


    def new_year(self):
        self._age += 1

    @property
    def get_fitness(self):
        if self._weight < 0:
            return 0
        else:
            self._fitness = fitness_calc()
        
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