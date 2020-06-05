__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .animals import Carnivore, Herbivore
from typing import Union
from typing import List

import random


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

    """# TODO add None
    def add_animals(self, carnivore: int, herbivore: int) -> None: # TODO Add optional animal parameter
        if carnivore is not None:
            for _ in range(carnivore):
                self.carnivores.append(Carnivore())
                self.n_carnivores += 1

                
        if herbivore is not None:
            for _ in range(herbivore):
                self.herbivores.append(Herbivore())
                self.n_herbivores += 1"""

    def add_animal(self, animal):
        if type(animal) == Herbivore:
            self.herbivores.append(animal)
            self.n_carnivores += 1
        elif type(animal) == Carnivore:
            self.carnivores.append(animal)
            self.n_herbivores += 1
        else:
            raise ValueError("species is neither carnivore er herbivore")

    def remove_animals(self):
        raise NotImplementedError("Remove animals is not implemented yet")


    def new_year(self):
        reverse_sort_c = sorted(self.carnivores, key= lambda animal: animal.get_fitness(), reverse=True)
        for c in reverse_sort_c:
            print(c)

        sorted_h = sorted(self.herbivores, key= lambda animal: animal.get_fitness(), reverse=False)
        for h in sorted_h:
            print(h)


        


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
