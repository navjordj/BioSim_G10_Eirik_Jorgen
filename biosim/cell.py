__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .animals import Carnivore, Herbivore
from typing import Union
from typing import List

import random

# TODO implement test
def p_eat(phi_carn, phi_herb, delta_phi_max):
    if phi_carn <= phi_herb:
        return 0
    elif (0 < phi_carn - phi_herb) and (phi_carn - phi_herb < delta_phi_max):
        return (phi_carn - phi_herb)/(delta_phi_max)
    else:
        return 1


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
    def eat_herbivore(self) -> None:
        fodder_left: Union[int, float] = self.fodder
        shuffled_herbivores = self.herbivores.copy() # Avoid shuffling original herbivore list
        random.shuffle(shuffled_herbivores) # TODO refactor code

        for herbi in shuffled_herbivores:
            if fodder_left == 0:
                break # Break out of loop when there is no food left
            elif fodder_left - herbi.params["F"] < 0:
                fodder_eaten = fodder_left
            else:
                fodder_eaten = herbi.params["F"]

            fodder_left -= fodder_eaten
            herbi.update_weight(herbi.params["beta"] * fodder_eaten)

    def eat_carnivore(self) -> None:

        reverse_sort_c = sorted(self.carnivores, key= lambda animal: animal.get_fitness(), reverse=True)
        sorted_h = sorted(self.herbivores, key= lambda animal: animal.get_fitness(), reverse=False)

        for i, carni in enumerate(reverse_sort_c):
            f_eaten: Union[int, float] = 0
            for j, herbi in enumerate(sorted_h):
                if herbi.alive:
                    p = p_eat(carni.get_fitness(), herbi.get_fitness(), carni.params["delta_phi_max"])
                    if random.random() < p:
                        herbi.alive = False
                        print(f'Herbivore nr. {j} got eaten by Carnivore nr. {i}')
                        f_eaten +=  herbi.weight
                        carni.update_weight(carni.params["beta"] * f_eaten)
                        #print(f'Carnivore nr. {i} has eaten {f_eaten} kg herbi')
                        if f_eaten >= carni.params["F"]: # TODO Check if there are leftovers
                            break



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

        if type(self) == Lowland or type(self) == Highland:
            self.eat_herbivore()


        self.eat_carnivore()

        
        # MIGRATION:
        # not implemented yet

        # TODO Check when the age increases
        # Increase age of all animals
        for h in self.herbivores:
            h.new_year()
        
        for c in self.carnivores:
            c.new_year()

        


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
