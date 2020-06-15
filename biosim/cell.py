__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .animals import Carnivore, Herbivore
from typing import Union, List, Dict

import numpy as np
import random
np.random.seed(1)


# TODO implement test
# TODO move insie carnivore
def p_eat(phi_carn: float, phi_herb: float, delta_phi_max: Union[int, float]) -> Union[int, float]:
    if phi_carn <= phi_herb:
        return 0
    elif (0 < phi_carn - phi_herb) and (phi_carn - phi_herb < delta_phi_max):
        return (phi_carn - phi_herb) / (delta_phi_max)
    else:
        return 1


class Cell:

    max_fodder: Union[float, int] = 0

    def __init__(self) -> None:
        self.carnivores: List[Carnivore] = []
        self.herbivores: List[Herbivore] = []

        self.n_carnivores: int = 0
        self.n_herbivores: int = 0

        self.allowed_move_to: bool = True
        self.fodder = self.max_fodder

    def __str__(self):
        return f'{type(self)} \n number of carnivores: {len(self.carnivores)} \n number of herbivores: {len(self.herbivores)}'

    # TODO make it so it's possible to move to then move
    # TODO evaluate if this function is necessary
    def migrate(self) -> bool:

        if self.allowed_move_to is False:
            return False
        else:
            return True

    def remove_animal(self, animal): # TODO: add type
        """
        Removes wanted animal from either self.herbivores or self.carnivores.
        Updates number of animals afterwards

        Parameters
        ----------
        animal: Class

        """
        try:
            if type(animal) == Herbivore:
                self.herbivores.remove(animal)
                self.n_herbivores = len(self.herbivores)
            else:
                self.carnivores.remove(animal)
                self.n_carnivores = len(self.carnivores)
        except ValueError as error:
            print(error)

    def eat_herbivore(self) -> None:
        """
        Shuffles the herbivore list and iterates through all, where the first one in the
        shuffled list eats first, then the second and so on. When all the fodder is eaten will the
        remaining of the herbivores not eat this year.
        A herbivore will stop eating when it have eaten F amount of fodder or there is nothing left
        """
        shuffled_herbivores: List[Herbivore] = self.herbivores.copy()  # Avoid shuffling original herbivore list
        np.random.shuffle(shuffled_herbivores)  # TODO refactor code
        # TODO test if fodder newer gets below zero
        for herbi in shuffled_herbivores:
            appetite = herbi.params["F"]
            food_left = self.fodder
            f_eaten = 0.

            if food_left <= 0:
                break
            elif appetite < food_left:
                f_eaten += appetite
            else:
                f_eaten += food_left

            self.fodder -= f_eaten
            herbi.update_weight(herbi.params["beta"] * f_eaten)

    def eat_carnivore(self) -> None:
        """
        Sort carnivores after fitness, the fittest first and least fittest last.
        Sort herbivores after fitness, the least fittest first and the fittest last.
        Iterates through the carnivores and the carnivore itterates over the herbivores.
        Every carnivore have an opportunity to kill a herbivore once a year. A carnivore will stop
        'hunting' the carnivore have eaten F amount of fodder.
        Can only hunt on herbivores in the same cell
        """
        self.remove_dead_herbivore()

        reverse_sort_c: List[Carnivore] = sorted(self.carnivores,
                                                 key=lambda animal: animal.get_fitness(),
                                                 reverse=True)
        sorted_h: List[Herbivore] = sorted(self.herbivores, key=lambda animal: animal.get_fitness(),
                                           reverse=False)
        for carni in reverse_sort_c:
            appetite = carni.params["F"]
            f_eaten = 0.
            for herbi in sorted_h:
                if f_eaten >= appetite:
                    break
                elif random.random() < p_eat(carni.get_fitness(), herbi.get_fitness(), carni.params["delta_phi_max"]):
                    f_wanted = appetite - f_eaten
                    if herbi.weight <= f_wanted:
                        f_eaten += herbi.weight
                        herbi.alive = False
                    else:
                        f_eaten += f_wanted
                        herbi.alive = False
            self.remove_dead_herbivore() # TODO fix so it will make sense inside the rest fo the functions and classes
            carni.update_weight(carni.params["beta"] * f_eaten)

    # TODO add type
    def add_animal(self, animal: Union[Herbivore, Carnivore],
                   age: Union[int, None] = None,
                   weight: Union[int, float, None] = None) -> None:  # choose Any because hard to name type
        """
        Takes in a type of animal, either Herbivore or Carnivore, and add's the respected animal to
        it's animal list (either self.herbivores or self.carnivores)
        Updates the amount of animals afterwards
        Parameters
        ----------
        animal: Class
            An animal subclass (Herbivore or Carnivore)
        age: int, None
            sets the age of the animal, if None it will be sat to 0
        weight: int, float, None
            sets the weight of the animal, if None it will be sat after a normal distribution
        """
        if animal == 'Herbivore':
            self.herbivores.append(Herbivore(age=age, weight=weight))
            self.n_herbivores += 1
        elif animal == 'Carnivore':
            self.carnivores.append(Carnivore(age=age, weight=weight))
            self.n_carnivores += 1
        else:
            raise ValueError("species is neither carnivore er herbivore")

    # TODO Add test for removing eaten herbivores
    # TODO set remove_dead_herbivores and remove_dead_carnivores into one function
    def remove_dead_herbivore(self) -> None:
        """
        Removes every herbivore that have self.alive = False.
        Updates number of herbivores afterwards
        """
        keep_herbivores: List[Herbivore] = []
        for h in self.herbivores:
            if h.alive == True:
                keep_herbivores.append(h)
        self.herbivores = keep_herbivores.copy()
        self.n_herbivores = len(keep_herbivores)

    def remove_dead_carnivore(self) -> None:
        keep_carnivores: List[Carnivore] = []
        for c in self.carnivores:
            if c.alive == True:
                keep_carnivores.append(c)
        self.carnivores = keep_carnivores
        self.n_carnivores = len(keep_carnivores)

    # TODO set carnivore_babies and herbivore_babies in same function
    # TODO: maybe make the new animal using the add_animal function?
    def carnivore_babies(self) -> None:
        """
        Checks if there are more than one animal in one cell, if so it will go trough all animals
        in the cell and calculate the probability for the animal to give birth, if it will give
        birth it will make a new animal and put it inside it's respected animal list.
        The mother of the child will lose weight after given birth
        """
        carnivore_babies: List[Carnivore] = []
        if self.n_carnivores >= 2:
            for carni in self.carnivores:
                give_birth = carni.give_birth(self.n_carnivores)
                if give_birth:
                    baby_carnivore = Carnivore()
                    baby_weight = baby_carnivore.weight
                    mother_weight_change = - carni.params["xi"] * baby_weight

                    if mother_weight_change > carni.weight:
                        print("no baby born")
                        continue
                    else:
                        carni.update_weight(mother_weight_change)
                        carnivore_babies.append(baby_carnivore)
        self.carnivores.extend(carnivore_babies)
        self.n_carnivores = self.n_carnivores + len(carnivore_babies)

    def herbivore_babies(self) -> None:
        herbivore_babies: List[Herbivore] = []
        if self.n_herbivores >= 2:
            for herbi in self.herbivores:
                give_birth = herbi.give_birth(self.n_herbivores)
                if give_birth:
                    baby_herbivore = Herbivore()
                    baby_weight = baby_herbivore.weight
                    mother_weight_change = -herbi.params["xi"] * baby_weight
                    if mother_weight_change > herbi.weight:
                        print('no baby born')
                        continue
                    else:
                        herbi.update_weight(mother_weight_change)
                        herbivore_babies.append(baby_herbivore)
        self.herbivores.extend(herbivore_babies)
        self.n_herbivores = self.n_herbivores + len(herbivore_babies)

    # TODO: maybe put both the death functions together
    def prob_death_herb(self) -> None:
        """
        Looks at the probability of each animal to die, if it's likely, the dead animal will
        be removed
        """
        for herb in self.herbivores:
            if herb.should_die():
                herb.alive = False

        self.remove_dead_herbivore()

    def prob_death_carni(self) -> None:
        for carni in self.carnivores:
            if carni.should_die():
                carni.alive = False

        self.remove_dead_carnivore()


class Desert(Cell):
    """
    Subclass of the superclass Cell
    """
    def __init__(self) -> None:
        super().__init__()


class Highland(Cell):
    """
    Attributes
    ----------
    params: dict
        have what the max mount of fodder available in cell
    """

    params = {'f_max': 300.0}

    def __init__(self) -> None:
        super().__init__()
        self.fodder = self.grow()

    def grow(self) -> Union[int, float]:
        """
        Updates the amount of fodder inside the cell. Will happen yearly
        Returns
        -------
        self.params['f_max']
            max amount of fodder inside the cell
        """
        return self.params['f_max']

    @classmethod
    def set_parameters(cls, new_parameters: Dict[str, Union[int, float]]) -> None:  # TODO add type
        """
        Takes in a dict with which parameters you want to change and the new amount
        Parameters
        ----------
        new_parameters: dict
            key is a string with of which parameter you want to change, and the value is either a
            int or a float of the new amount
        """
        for key in new_parameters:
            if new_parameters[key] >= 0:
                cls.params[key] = new_parameters[key]
            else:
                raise ValueError('max_fodder must be a positive number')


class Lowland(Cell):
    """
    Attributes
    ----------
    params: dict
        have what the max mount of fodder available in cell
    """

    params = {'f_max': 800.0}

    def __init__(self) -> None:
        super().__init__()
        self.fodder = self.grow()

    def grow(self) -> Union[int, float]:
        """
        Updates the amount of fodder inside the cell. Will happen yearly
        Returns
        -------
        self.params['f_max']
        max amount of fodder inside the cell
        """
        return self.params['f_max']

    @classmethod
    def set_parameters(cls, new_parameters: Dict[str, Union[int, float]]) -> None: # TODO add type
        """
        Takes in a dict with which parameters you want to change and the new amount
        Parameters
        ----------
        new_parameters: dict
        key is a string with of which parameter you want to change, and the value is either a
        int or a float of the new amount
        """
        for key in new_parameters:
            if new_parameters[key] >= 0:
                cls.params[key] = new_parameters[key]
            else:
                raise ValueError('max_fodder must be a positive number')


class Water(Cell):
    """
    Subclass of the superclass Cell
    """
    def __init__(self) -> None:
        super().__init__()
        self.allowed_move_to = False
