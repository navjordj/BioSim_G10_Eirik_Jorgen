__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import random

def fitness_calc() -> float:
    pass

class Animal:

    def __init__(self, age, weight=None):
        self._age = age
        self._fitness = fitness
        if weight == None:
            pass
        else:
            self._weight = weight
        

    @staticmethod
    def increase_age(self):
        self.age += 1
        return True

    def update_weight(self, change):
        self.weight += change


    def new_year(self):
        self._age += 1

    @property
    def get_fitness(self):
        if self._weight < 0:
            return 0
        else:
            self._fitness = fitness_calculation()
        
        return self._fitness


    @property
    def get_age(self):
        return self._age

    @property
    def get_weight(self):
        return self._weight