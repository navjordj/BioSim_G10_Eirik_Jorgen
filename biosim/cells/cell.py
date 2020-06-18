__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'

from biosim.animals.carnivore import Carnivore
from biosim.animals.herbivore import Herbivore

from typing import Union, List

import numpy as np

class Cell:
    max_fodder: Union[float, int] = 0

    def __init__(self) -> None:

        # Lists containing the carnivores and herbivores in every cell
        self.carnivores: List[Carnivore] = []
        self.herbivores: List[Herbivore] = []

        # Cached number of animals for both species.
        self.n_carnivores: int = 0
        self.n_herbivores: int = 0

        self.allowed_move_to: bool = True
        self.fodder = self.max_fodder

        # Number of infected animals if corona pandemic
        self.infect_related_death_herb: int = 0
        self.infect_related_death_carn: int = 0

    def __repr__(self):
        return f'{type(self)} \n number of carnivores: {len(self.carnivores)} \n ' \
               f'number of herbivores: {len(self.herbivores)}'

    def eat_herbivore(self) -> None:
        """
        Shuffles the herbivore list and iterates through all, where the first one in the
        shuffled list eats first, then the second and so on. When all the fodder is eaten will the
        remaining of the herbivores not eat this year.
        A herbivore will stop eating when it have eaten F amount of fodder or there is nothing left
        """
        shuffled_herbivores: List[
            Herbivore] = self.herbivores.copy()  # Avoid shuffling original herbivore list
        np.random.shuffle(shuffled_herbivores)  # TODO refactor code
        # TODO test if fodder newer gets below zero
        np.random.shuffle(shuffled_herbivores)

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
        Iterates through the carnivores and the carnivore iterates over the herbivores.
        Every carnivore have an opportunity to kill a herbivore once a year. A carnivore will stop
        'hunting' the carnivore have eaten F amount of fodder.
        Can only hunt on herbivores in the same cell
        """
        # TODO: test break bit
        self.remove_dead_animals()

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
                elif np.random.random() < carni.p_eat(carni.get_fitness(), herbi.get_fitness(),
                                                      carni.params["DeltaPhiMax"]):
                    f_wanted = appetite - f_eaten
                    if herbi.weight <= f_wanted:
                        f_eaten += herbi.weight
                        herbi.alive = False
                    else:
                        f_eaten += f_wanted
                        herbi.alive = False
            carni.update_weight(carni.params["beta"] * f_eaten)

    def add_animal(self, animal: str,
                   age: Union[int, None] = None,
                   weight: Union[
                       int, float, None] = None) -> None:
        """
        Takes in a type of animal, either Herbivore or Carnivore, and add's the respected animal to
        it's animal list (either self.herbivores or self.carnivores)
        Updates the amount of animals afterwards
        Parameters
        ----------
        animal: str
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

    def remove_dead_animals(self) -> None:
        """
        Removes every herbivore that have self.alive = False.
        Updates number of herbivores afterwards
        """
        keep_herbivores: List[Herbivore] = []

        self.n_herbivores = 0
        self.n_carnivores = 0

        for h in self.herbivores:
            if h.alive is True:
                keep_herbivores.append(h)
                self.n_herbivores += 1

        keep_carnivores: List[Carnivore] = []
        for c in self.carnivores:
            if c.alive is True:
                keep_carnivores.append(c)
                self.n_carnivores += 1

        self.herbivores = keep_herbivores
        self.carnivores = keep_carnivores

    def animal_babies(self) -> None:
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
                    carni.update_weight(mother_weight_change)
                    carnivore_babies.append(baby_carnivore)
                    self.n_carnivores += 1

        herbivore_babies: List[Herbivore] = []
        if self.n_herbivores >= 2:
            for herbi in self.herbivores:
                give_birth = herbi.give_birth(self.n_herbivores)
                if give_birth:
                    baby_herbivore = Herbivore()
                    baby_weight = baby_herbivore.weight
                    mother_weight_change = -herbi.params["xi"] * baby_weight
                    herbi.update_weight(mother_weight_change)
                    herbivore_babies.append(baby_herbivore)
                    self.n_herbivores += 1

        self.carnivores.extend(carnivore_babies)
        self.herbivores.extend(herbivore_babies)

    def death_animals(self) -> None:
        """
        Looks at the probability of each animal to die, if it's likely, the dead animal will
        be removed
        """
        for herb in self.herbivores:
            prob, infected = herb.should_die()
            if prob is True:
                herb.alive = False
                if infected is True:
                    self.infect_related_death_herb += 1
            herb.infected = False

        for carni in self.carnivores:
            prob, infected = carni.should_die()
            if prob is True:
                carni.alive = False
                if infected is True:
                    self.infect_related_death_carn += 1
            carni.infected = False

        self.remove_dead_animals()

    def infected_animals(self) -> bool:
        infected_in_cell = False
        for herb in self.herbivores:
            if herb.infected is True:
                infected_in_cell = True

        for carn in self.carnivores:
            if carn.infected is True:
                infected_in_cell = True

        if infected_in_cell is True:
            for herb in self.herbivores:
                herb.infected = True
            for carn in self.carnivores:
                carn.infected = True
        return infected_in_cell

    def new_year(self) -> None:
        for herb in self.herbivores:
            herb.new_year()
        for carn in self.carnivores:
            carn.new_year()
