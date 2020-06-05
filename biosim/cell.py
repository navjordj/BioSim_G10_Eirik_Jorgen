__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .animals import Carnivore, Herbivore
from typing import Union
from typing import List


class Cell:
    def __init__(self) -> None:
        self.carnivores: List[Carnivore] = []
        self.herbivores: List[Herbivore] = []
        self.fodder: Union[float, int] = 0
        self.allowed_move_to = True
        self.n_carnivores: int = 0
        self.n_herbivores: int = 0


    def __str__(self):
        return f'{type(self)} \n number of carnivores: {self.n_carnivores} \n number of herbivores: {self.n_herbivores}'

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
            if self.fodder == 0:
                eaten[animal] = self.fodder
            elif self.fodder > amount:
                eaten[animal] = amount
                self.fodder -= amount
            elif self.fodder <= amount:
                eaten[animal] = amount - self.fodder
                self.fodder = 0

        return True

    # TODO add None
    def add_animals(self, carnivore: List, herbivore: List) -> None: # TODO Add optional animal parameter
        if carnivore is not None:
            for animal in carnivore:
                self.carnivores.append(animal)
                self.n_carnivores += 1
        if herbivore is not None:
            for animal in herbivore:
                self.herbivores.append(animal)
                self.n_herbivores += 1

    def remove_animals(self):
        raise NotImplementedError("Remove animals is not implemented yet")


class Desert(Cell):
    def __init__(self) -> None:
        super().__init__()


class Highland(Cell):

    max_fodder = 300

    def __init__(self) -> None:
        super().__init__()
        self.fodder = self.max_fodder

    def grow(self) -> None:
        self.fodder = self.max_fodder


class Lowland(Cell):

    max_fodder = 800

    def __init__(self) -> None:
        super().__init__()
        self.fodder = self.max_fodder

    def grow(self) -> None:
        self.fodder = self.max_fodder


class Water(Cell):
    def __init__(self) -> None:
        super().__init__()
        self.allowed_move_to = False
