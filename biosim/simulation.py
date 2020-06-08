__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .cell import Lowland, Highland
from .animals import Herbivore, Carnivore

import numpy as np
from typing import Dict

class BioSim:
    def __init__(
        self,
        seed,
        ini_pop,

        island_map=None,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20} 

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        # self.year = 0

        self.island_map = [Lowland()]
        self.add_population(ini_pop)
        np.random.seed(seed)


    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        for i in range(num_years):
            print(f'Year {i}: ')
            for c in self.island_map:
                c.grow()
                c.new_year()
            print(c)
            # self.year += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        cell = self.island_map[0]

        for species in population:
            if species["species"] == 'Herbivore':
                h = Herbivore(age=species["age"], weight=species["weight"])
                cell.add_animal(h)

            elif species["species"] == 'Carnivore':
                c = Carnivore(age=species["age"], weight=species["weight"])
                cell.add_animal(c)
            else:
                raise ValueError("species is neither carnivore er herbivore") # TODO add test

    @property
    def year(self):
        """Last year simulated."""
        # return self.year

        

    @property
    def num_animals(self) -> int:
        """Total number of animals on island."""
        animal_count = self.num_animals_per_species
        return animal_count["herbivores"] + animal_count["carnivores"]

    @property
    def num_animals_per_species(self) -> Dict[str, int]:
        """Number of animals per species in island, as dictionary."""
        animal_count: Dict[str, int] = {"herbivores": 0, "carnivores": 0} # TODO Refactor with standard values
        
        for c in self.island_map:
            animal_count["herbivores"] += len(c.herbivores)
            animal_count["carnivores"] += len(c.carnivores)
        
        return animal_count

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
