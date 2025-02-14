__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'

from math import exp
from typing import Union, Dict, Tuple
import numpy as np


class Animal:
    """Documentation for Animal superclass implemented using the specifications in
    PEAP requirements

    """
    params: dict = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.2,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
        "DeltaPhiMax": None,
        "infected": False
    }

    def __init__(self, age=None, weight=None):
        """Constructor for animal superclass. Herbivore and Carnivore inherits from this class

        Parameters
        ----------
        age : int, optional
            Age of a new animal. If not specified, age of a new animal will be 0
        weight : Union[int, float], optional
            Weight of a new animal. If not specified, weight of a new animal will be normally
            distributed using w_birth and sigma_birth parameters.
        """

        if age is None:
            self.age: int = 0
        else:
            self.age: int = age
        if weight is None:
            self.weight: float = self._initialize_weight()
        else:
            self.weight: float = weight

        self.fitness: Union[int, float] = self.get_fitness()
        self.alive: bool = True
        self.has_migrated: bool = False
        self.infected: bool = self.params['infected']  # can choose to set animals to be
        # infected by the virus

    def __repr__(self) -> str:
        """method for how a animal should be represented when printed to the console

        Returns
        -------
        str
            String to be printed out
        """
        return f'Type: {type(self)} \n \
                 Age: {self._age} \n \
                 Fitness: {self.get_fitness()}'  # pragma: no cover

    @classmethod
    def set_params(cls, new_parameters: Dict[str, Union[int, float]]) -> None:
        """Set internal parameters for animal class/ subclass

        Parameters
        ----------
        new_parameters : Dict[str, Union[int, float]]
            Dictionary containing the keys of the parameters to be changed
            and the corresponding values

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

    def increase_age(self) -> None:

        self._age += 1

    def should_die(self) -> Tuple[bool, bool]:
        """Returns a boolean saying if the animal should die or not

        Returns
        -------
        Tuple[bool, bool]
            Boolean representing if the animal should die or not and if it was infected
        """
        prob_death: Union[int, float] = 0
        if self._weight <= 0:
            return True, False
        else:
            if self.infected is True:
                # total death count and infected count of the COVID-19 virus in the world (17.06.20)
                prob_death += 440290 / 8061550
            p: float = self.params["omega"] * (1 - self.fitness)
            prob_death += p

            return np.random.random() < prob_death, self.infected

    def give_birth(self, N: int) -> bool:
        """Returns a boolean saying if the animal should give birth or not.
        Higher possibility to die if infected by the virus
        Parameters
        ----------
        N : int
            Number of animals of the same species in the cell

        Returns
        -------
        bool
            Boolean representing of the animal should give birth or not
        """
        # Can only make a baby once a year, if migrated to a cell it will not make baby in
        # the new cell
        if self.has_migrated is False:
            if self._weight < self.params["zeta"] * \
             (self.params["w_birth"] + self.params["sigma_birth"]):
                return False

            p: Union[int, float] = min(1, self.params["gamma"] * self.fitness * (N - 1))
            if np.random.random() < p:
                return True
            else:
                return False
        else:
            return False

    def eat(self, intake: Union[int, float]) -> None:
        """
        Takes in a certain amount of fodder. Calculates and updates weight given by beta * intake.

        Parameters
        ----------
        intake : Union[int, float]
            How much fodder the animal should eat

        Raises
        ------
        ValueError
            Raises ValueError if the amount of fodder eaten is negative
        """
        # When an animal has migrated, it will not eat again
        if self.has_migrated is False:
            if intake < 0:
                raise ValueError("Cant eat negative amount")
            else:
                weight_change: float = self.params["beta"] * intake
                self.update_weight(weight_change)

    def update_weight(self, change: float) -> None:
        """Updates the weight of the animal and recalculates fitness

        Parameters
        ----------
        change : float
            The weight change of the animal
        """
        self._weight += change
        self.fitness = self.get_fitness()

    def new_year(self) -> None:
        """Increase age by one year and decrease weight by eta * weight
        """
        self.has_migrated = False
        self.increase_age()
        weight_change: float = -self.params["eta"] * self._weight
        self.update_weight(weight_change)
        self.fitness = self.get_fitness()

    def get_fitness(self) -> float:
        """Returns the current fitness of a animal

        Returns
        -------
        float
            Fitness of a animal
        """
        if self._weight < 0:
            return 0
        else:
            new_fitness = self._fitness_calc(self._age,
                                             self.params["a_half"],
                                             self.params["phi_age"],
                                             self._weight,
                                             self.params["w_half"],
                                             self.params["phi_weight"])

        return new_fitness

    def _initialize_weight(self) -> float:
        """Initializes the weight using a normal distribution

        Returns
        -------
        float
            Initial weight of the animal
        """
        return np.random.normal(self.params["w_birth"], self.params["sigma_birth"])

    def will_migrate(self) -> bool:
        """Returns a boolean representing if a animal should migrate or not

            Probability of migration is given by the following equation:


        Returns
        -------
        bool
            Boolean representing of the animal should migrate or not
        """
        if self.has_migrated is False:
            prob = self.params["mu"] * self.fitness
            if np.random.rand() < prob:
                self.has_migrated = True
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def _fitness_calc(a: float,
                      a_half: float,
                      phi_age: float,
                      w: float,
                      w_half: float,
                      phi_weight: float) -> float:
        """Helper function for calculating the current fitness of animal

        Parameters
        ----------
        a : float
            [description]
        a_half : float
            [description]
        phi_age : float
            [description]
        w : float
            [description]
        w_half : float
            [description]
        phi_weight : float
            [description]

        Returns
        -------
        float
            The current fitness of a animal
        """
        def _q(x: float, x_half: float, phi: float, sign: int) -> float:
            return 1 / (1 + exp(sign * phi * (x - x_half)))

        return _q(a, a_half, phi_age, 1) * _q(w, w_half, phi_weight, -1)

    @property
    def age(self) -> int:
        """Getter for age of a animal

        Returns
        -------
        int
            The age of the animal
        """
        return self._age

    @age.setter
    def age(self, new_age: int) -> None:
        """Setter for the age of a animal

        Parameters
        ----------
        new_age : int
            The new age of the animal
        """
        self._age = new_age

    @property
    def weight(self) -> float:
        """Getter for the weight of a animal

        Returns
        -------
        float
            The weight of a animal
        """
        return self._weight

    @weight.setter
    def weight(self, new_weight: float) -> None:
        """Setter for the weight of a animal

        Parameters
        ----------
        new_weight : float
            The new weight of the animal
        """
        self._weight = new_weight
