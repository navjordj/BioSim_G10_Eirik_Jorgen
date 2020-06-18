__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no, navjordj@gmail.com'

from .cell import Cell

from typing import Union, Dict


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
        self.fodder = self.params['f_max']
        return self.fodder

    @classmethod
    def set_parameters(cls, new_parameters: Dict[str, Union[int, float]]) -> None:
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
