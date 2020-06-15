__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from .cell import Lowland, Highland, Water, Desert
from .animals import Herbivore, Carnivore
from .island import Island
from .viz import Viz

from .plotting import plot_map

import numpy as np
# import matplotlib.pyplot as plt
from typing import Dict, Union
import matplotlib.pyplot as plt

set_params_simulation
import pickle
master

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
            save_name = None
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
        np.random.seed(seed)
        if save_name is None:
            self.island_map = Island(map_str=island_map)
        else:
            self.island_map = self.load_simlation(save_name)

        self.add_population(ini_pop)

    set_params_simulation
    @staticmethod
    def set_animal_parameters(species, params):
    def set_animal_parameters(self, species, params):
        master
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        animals = {
            'Herbivore': Herbivore,
            'Carnivore': Carnivore
        }
        animals[species].set_params(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        landscape_types = {
            'L': Lowland,
            'H': Highland
        }
        landscape_types[landscape].set_parameters(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """

        viz = Viz(self.island_map, num_years)

        # TODO fix map.map.map.map
        for year in range(num_years):
            print(f'Year {year}: ')

            # TODO make a proper iterator
            self.island_map.new_year()
            self.island_map.num_herbivores_data.append(self.num_animals_per_species["herbivores"])
            self.island_map.num_carnivores_data.append(self.num_animals_per_species["carnivores"])
            self.island_map.year += 1

            # if self.island_map.year % 5 == 0:
            viz.update_fig(self.island_map)
            print(self.num_animals_per_species)
            # print(self.num_animals_per_species)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        # [{loc: (1, 1), pop: [{species: Herbi, age: 4, weight: 3}]}]
        for cell in population:
            loc = cell["loc"]
            pop = cell["pop"]

            for animal in pop:
                # TODO age and weight might be none
                type_animal = animal["species"]
                age = animal["age"]
                weight = animal["weight"]
                # print(type_animal, age, weight)
                if type(self.island_map.map[loc[0] - 1][loc[1] - 1]) == Water:
                    raise ValueError(f"Cant add animals on water landscape ({loc[0], loc[1]})")
                else:
                    self.island_map.map[loc[0] - 1][loc[1] - 1].add_animal(animal=type_animal,
                                                                           age=age, weight=weight)

    def save_simulation(self, filename):
        with open(filename + '.pkl', 'wb') as file:
            pickle.dump(self.island_map, file)

    def load_simlation(self, filename):
        with open(filename + '.pkl', 'rb') as file:
            return pickle.load(file)

    @property
    def year(self):
        """Last year simulated."""
        # return self.year

    # TODO: tyr to use these functions inside viz.py instead of doing what we are doing now
    @property
    def num_animals(self) -> int:
        """Total number of animals on island."""
        animal_count = self.num_animals_per_species
        return animal_count["herbivores"] + animal_count["carnivores"]

    @property
    def num_animals_per_species(self) -> Dict[str, int]:
        """Number of animals per species in island, as dictionary."""
        animal_count: Dict[str, int] = {"herbivores": 0,
                                        "carnivores": 0}  # TODO Refactor with standard values
        for i, row in enumerate(self.island_map.map):
            for j, cell in enumerate(row):
                animal_count["herbivores"] += len(cell.herbivores)
                animal_count["carnivores"] += len(cell.carnivores)

        return animal_count

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
