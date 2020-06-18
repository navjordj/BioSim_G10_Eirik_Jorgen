__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'

from .animal import Animal

from typing import Union


class Carnivore(Animal):
    """Documentation for Carnivore
    """
    params: dict = {
            "w_birth": 6.0,
            "sigma_birth": 1.0,
            "beta": 0.75,
            "eta": 0.125,
            "a_half": 40.0,
            "phi_age": 0.3,
            "w_half": 4.0,
            "phi_weight": 0.4,
            "mu": 0.4,
            "gamma": 0.8,
            "zeta": 3.5,
            "xi": 1.1,
            "omega": 0.8,
            "F": 50.0,
            "DeltaPhiMax": 10,
            "infected": False
    }

    def __init__(self, age=None, weight=None) -> None:
        super().__init__(age, weight)

    @staticmethod
    def p_eat(phi_carn: float,
              phi_herb: float,
              DeltaPhiMax: Union[int, float]) -> Union[int, float]:
        """
        Probability for a carnivore to eat a herbivore
        Parameters
        ----------
        phi_carn:
            fitness carnivore
        phi_herb:
            fitness herbivore
        DeltaPhiMax:
            a parameter that helps to decide if a carnivore eats a herbivore

        Returns
        -------
        A probability between 0 and 1
        """
        if phi_carn <= phi_herb:
            return 0
        elif (0 < phi_carn - phi_herb) and (phi_carn - phi_herb < DeltaPhiMax):
            return (phi_carn - phi_herb) / (DeltaPhiMax)
        else:
            return 1
