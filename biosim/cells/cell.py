__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

# from biosim.animals import carnovere.Carnivore, herbivore.Herbivore
from typing import Union
from typing import List


class Cell:
    def __init__(self) -> None:
        self.carnivores = []
        self.herbivores = []
        self.fodder = 0
        self.allowed_move_to = True

    # TODO make it so it's possible to move to then move
    def migrate(self) -> bool:

        if self.allowed_move_to is False:
            return False
        else:
            return True

    def set_parameters(self, fodder: Union[float, int]) -> None:
        if fodder >= 0:
            self.fodder = fodder
        else:
            raise ValueError('Fodder must be a positive number')

    # TODO must know what's inside Animals to do well
    def eat_herbivore(self, amount: Union[float, int]) -> bool:
        if self.herbivores == []:
            return False

        eaten = {}
        for animal in self.herbivores:
            if self.fodder is 0:
                eaten[animal] = self.fodder
            elif self.fodder > amount:
                eaten[animal] = amount
                self.fodder -= amount
            elif self.fodder <= amount:
                eaten[animal] = amount - self.fodder
                self.fodder = 0

        return True

    # TODO add None
    def add_animals(self, carnivore: List, herbivore: List) -> None:
        if carnivore is not None:
            for animal in carnivore:
                self.carnivores.append(animal)
        if herbivore is not None:
            for animal in herbivore:
                self.herbivores.append(animal)
