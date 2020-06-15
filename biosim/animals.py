__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from math import exp
from typing import Union, Dict
import numpy as np

np.random.seed(1)


def fitness_calc(a: float, a_half: float, phi_age: float,  w: float, w_half: float, phi_weight: float) -> float:

    def q(x: float, x_half: float, phi: float, sign: int) -> float:
        return 1 / (1 + exp(sign * phi*(x - x_half)))

    return q(a, a_half, phi_age, 1) * q(w, w_half, phi_weight, -1)


class Animal:
    # TODO Possible rewrite to normal attributes (no dict)

    """Animal superclass implemented using the specifications in https://github.com/heplesser/nmbu_inf200_june2020/blob/master/project_description/INF200_H19_BioSimJune_v2.pdf

    """
    params: dict = {
            "w_birth": 8.0,
            "sigma_birth": 1.5,
            "beta": 0.9,
            "eta": 0.05,
            "a_half": 40.0,
            "phi_age": 0.2,
            "weight_half": 10.0,
            "phi_weight": 0.1,
            "mu": 0.25,
            "gamma": 0.2,
            "zeta": 3.5,
            "xi": 1.2,
            "omega": 0.4,
            "F": 10.0,
            "delta_phi_max": None
        }
    
    def __init__(self, age=None, weight=None):  # TODO Fix standard weight value
        """Constructor for animal superclass. Herbivore and Carnivore inherits from this class

        Parameters
        ----------
        age : int, optional
            Age of a new animal. If not specified, age of a new animal will be 0
        weight : Union[int, float], optional
            Weight of a new animal. If not specified, weight of a new animal will be normally distributed using w_birth and sigma_birth parameters.
        """

        if age == None:
            self.age: int = 0
        else:
            self.age: int = age
        if weight == None:
            self.weight: float = self.initialize_weight()
        else:
            self.weight: float = weight

        self.fitness = self.get_fitness()
        self.alive = True  # Might not be necessary
        self.has_migrated = False

    def __str__(self) -> str:
        """method for how a animal should be represented when printed to the console

        Returns
        -------
        str
            String to be printed out
        """
        return f'Type: {type(self)} \n Age: {self.age} \n Fitness: {self.get_fitness()}' # pragma: no cover

    @classmethod
    def set_params(cls, new_parameters: Dict[str, Union[int, float]]) -> None:
        """Set internal parameters for animal class/ subclass

        Parameters
        ----------
        new_parameters : Dict[str, Union[int, float]]
            Dictionary containing the keys of the parameters to be changed and the corresponding values

        Raises
        ------
        ValueError
            Raises ValueError if key is  not in self.params
        """
        for key in new_parameters:
            if new_parameters[key] >= 0:
                if key in cls.params.keys():
                    cls.params[key] = new_parameters[key]
                else:
                    raise ValueError(f'Key {key} is not a key in class parameters')
            else:
                raise ValueError(f'Key for {key} cant be negative ({new_parameters[key]}')
    # TODO: Return value? Bool to confirm success?
    def increase_age(self) -> None:

        self.age += 1

    def should_die(self) -> bool:
        """Returns a boolean saying if the animal should die or not


        Returns
        -------
        bool
            Boolean representing if the animal should die or not
        """
        if self.weight <= 0:
            return True
        else:
            p: float = self.params["omega"] * (1 - self.fitness)
            return np.random.random() < p

    # TODO update correct type
    def give_birth(self, N: int) -> bool:
        """Returns a boolean saying if the animal should give birth or not

        Parameters
        ----------
        N : int
            Number of animals of the same species in the cell

        Returns
        -------
        bool
            Boolean representing of the animal should give birth or not
        """

        if self.weight < self.params["zeta"] * (self.params["w_birth"] + self.params["sigma_birth"]):
            return False

        p: Union[int, float] = min(1, self.params["gamma"]*self.fitness*(N-1))
        if np.random.random() < p:
            return True
        else:
            return False

    def eat(self, intake: Union[int, float]) -> None:
        """Takes in a certain amount of fodder. Calculates and updates weight given by beta * intake.


        Parameters
        ----------
        intake : Union[int, float]
            How much fodder the animal should eat

        Raises
        ------
        ValueError
            Raises ValueError if the amount of fodder eaten is negative
        """
        if intake < 0:
            raise ValueError("Cant eat negative amount")
        else:
            weight_change: float = self.params["beta"] * intake
            self.update_weight(weight_change)

    # TODO: Return value? Bool to confirm success?

    def update_weight(self, change: float) -> None:
        """Updates the weight of the animal and recalculates fitness

        Parameters
        ----------
        change : float
            The weight change of the animal
        """
        self.weight += change
        self.fitness = self.get_fitness()

    # TODO: Return value? Bool to confirm success?

    def new_year(self) -> None:
        """Increase age by one year and decrease weight by eta * weight
        """
        self.has_migrated = False
        self.age += 1
        weight_change: float = -self.params["eta"] * self.weight
        self.update_weight(weight_change)
        self.fitness = self.get_fitness()

    def get_fitness(self) -> float:
        """Returns the current fitness of a animal

        Returns
        -------
        float
            Fitness of a animal
        """
        if self.weight < 0:
            return 0
        else:
            self.fitness = fitness_calc(self.age, self.params["a_half"], self.params["phi_age"], 
                                         self.weight, self.params["weight_half"], self.params["phi_weight"] )

        return self.fitness

    # TODO Make private
    def initialize_weight(self) -> float:
        """Initializes the weight using a normal distribution

        Returns
        -------
        float
            Initial weight of the animal
        """
        return np.random.normal(self.params["w_birth"], self.params["sigma_birth"])

    # TODO add latex formula for probability
    def will_migrate(self) -> bool:
        """Returns a boolean representing if a animal should migrate or not

            Probability of migration is given by the following equation:
            

        Returns
        -------
        bool
            Boolean representing of the animal should migrate or not
        """
        if self.has_migrated is False:
            prob = self.params["mu"] * self.get_fitness()
            if np.random.rand() < prob:
                self.has_migrated = True
                return True
            else:
                return False
        else:
            return False


class Herbivore(Animal):
    params: dict = {
                "w_birth": 8.0,
                "sigma_birth": 1.5,
                "beta": 0.9,
                "eta": 0.05,
                "a_half": 40.0,
                "phi_age": 0.6,
                "weight_half": 10.0,
                "phi_weight": 0.1,
                "mu": 0.25,
                "gamma": 0.2,
                "zeta": 3.5,
                "xi": 1.2,
                "omega": 0.4,
                "F": 10.0,
                "delta_phi_max": None
            }
    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)


class Carnivore(Animal):
    params: dict = {
            "w_birth": 6.0,
            "sigma_birth": 1.0,
            "beta": 0.75,
            "eta": 0.125,
            "a_half": 40.0,
            "phi_age": 0.3,
            "weight_half": 4.0,
            "phi_weight": 0.4,
            "mu": 0.4,
            "gamma": 0.8,
            "zeta": 3.5,
            "xi": 1.1,
            "omega": 0.8,
            "F": 50.0,
            "delta_phi_max": 10
        }

    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)
