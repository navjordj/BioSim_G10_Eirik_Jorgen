__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .animals import Carnivore, Herbivore
from typing import Union, List, Any

import random


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
    def __init__(self) -> None:
        self.carnivores: List[Carnivore] = []
        self.herbivores: List[Herbivore] = []
        self.fodder: Union[float, int] = 0
        self.allowed_move_to: bool = True
        self.n_carnivores: int = 0
        self.n_herbivores: int = 0

    def __str__(self):
        return f'{type(self)} \n number of carnivores: {len(self.carnivores)} \n number of herbivores: {len(self.herbivores)}'

    # TODO make it so it's possible to move to then move
    # TODO evaluate if this function is necessary
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
        # fodder_left: Union[int, float] = self.fodder
        shuffled_herbivores: List[
            Herbivore] = self.herbivores.copy()  # Avoid shuffling original herbivore list
        random.shuffle(shuffled_herbivores)  # TODO refactor code
        # TODO test if fodder newer gets below zero
        for herbi in shuffled_herbivores:
            if self.fodder == 0:
                break  # Break out of loop when there is no food left
            elif self.fodder - herbi.params["F"] < 0:
                fodder_eaten = self.fodder
            else:
                fodder_eaten = herbi.params["F"]

            self.fodder -= fodder_eaten
            herbi.update_weight(herbi.params["beta"] * fodder_eaten)

    def eat_carnivore(self) -> None:

        reverse_sort_c: List[Carnivore] = sorted(self.carnivores,
                                                 key=lambda animal: animal.get_fitness(),
                                                 reverse=True)
        sorted_h: List[Herbivore] = sorted(self.herbivores, key=lambda animal: animal.get_fitness(),
                                           reverse=False)

        for i, carni in enumerate(reverse_sort_c):
            f_eaten: Union[int, float] = 0
            for j, herbi in enumerate(sorted_h):
                if herbi.alive:
                    p = p_eat(carni.get_fitness(), herbi.get_fitness(),
                              carni.params["delta_phi_max"])
                    if random.random() < p:
                        herbi.alive = False
                        f_eaten += herbi.weight
                        carni.update_weight(carni.params["beta"] * f_eaten)
                        if f_eaten >= carni.params["F"]:  # TODO Check if there are leftovers
                            break

    # TODO add type
    def add_animal(self, animal: Any, age=None, weight=None) -> None:  # choose Any because hard to name type
        if animal == 'Herbivore':
            self.herbivores.append(Herbivore(age=age, weight=weight))
            self.n_herbivores += 1
        elif animal == 'Carnivore':
            self.carnivores.append(Carnivore(age=age, weight=weight))
            self.n_carnivores += 1
        else:
            raise ValueError("species is neither carnivore er herbivore")

    # TODO Add test for removing eaten herbivores
    def remove_dead_herbivore(self) -> None:
        keep_herbivores: List[Herbivore] = []
        for h in self.herbivores:
            if h.alive == True:
                keep_herbivores.append(h)
        self.herbivores = keep_herbivores
        self.n_herbivores = len(keep_herbivores)

    def remove_dead_carnivore(self) -> None:
        keep_carnivores: List[Carnivore] = []
        for c in self.carnivores:
            if c.alive == True:
                keep_carnivores.append(c)
        self.carnivores = keep_carnivores
        self.n_carnivores = len(keep_carnivores)

    # TODO check for use of Carnivore()
    def carnivore_babies(self) -> None:
        carnivore_babies: List[Carnivore] = []
        if self.n_carnivores >= 2:
            for carni in self.carnivores:
                give_birth = carni.give_birth(self.n_carnivores)
                if give_birth:
                    baby_carnivore = Carnivore()
                    baby_weight = baby_carnivore.weight
                    carni.update_weight(- carni.params["xi"] * baby_weight)
                    carnivore_babies.append(baby_carnivore)
        self.carnivores.extend(carnivore_babies)
        self.n_carnivores = self.n_carnivores + len(carnivore_babies)

    # TODO check for use of Herbivore()
    def herbivore_babies(self) -> None:
        herbivore_babies: List[Herbivore] = []
        if self.n_herbivores >= 2:
            for herbi in self.herbivores:
                give_birth = herbi.give_birth(self.n_herbivores)
                if give_birth:
                    baby_herbivore = Herbivore()
                    baby_weight = baby_herbivore.weight
                    herbi.update_weight(- herbi.params["xi"] * baby_weight)
                    herbivore_babies.append(baby_herbivore)
        self.herbivores.extend(herbivore_babies)
        self.n_herbivores = self.n_herbivores + len(herbivore_babies)

    def prob_death_herb(self) -> None:
        for herb in self.herbivores:
            if herb.should_die():
                herb.alive = False

        self.remove_dead_herbivore()

    def prob_death_carni(self) -> None:
        for carni in self.carnivores:
            if carni.should_die():
                carni.alive = False

        self.remove_dead_carnivore()

    def new_year(self) -> None:
        # TODO make the fodder grow after they are done eating, either here or in the sim file
        if type(self) == Lowland or type(self) == Highland:
            self.eat_herbivore()

        self.eat_carnivore()

        self.remove_dead_herbivore()
        # MIGRATION:

        # Procreation:
        self.herbivore_babies()
        self.carnivore_babies()

        # Age animals one year:
        for h in self.herbivores:
            h.new_year()

        for c in self.carnivores:
            c.new_year()

        # DEATH
        self.prob_death_carni()
        self.prob_death_herb()

        self.n_herbivores = len(self.herbivores)
        self.n_carnivores = len(self.carnivores)


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
