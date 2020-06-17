__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

from biosim.animals import Herbivore, Carnivore
from biosim.cells import Lowland, Highland, Water, Desert
from biosim.island import Island
from biosim.viz import Viz

import numpy as np
from typing import Dict, Union
import matplotlib.pyplot as plt

import subprocess

import pickle
import csv
import os


class BioSim:
    def __init__(
            self,
            seed,
            ini_pop,
            plt_speed=None,
            island_map=None,
            ymax_animals=None,
            cmax_animals=None,
            hist_specs=None,
            img_base=None,
            img_fmt="png",
            movie_format=None,
            save_name=None,
            data_name=None

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
        if hist_specs is None:
            self.hist_specs = {'weight': None,
                              'age': None,
                              'fitness': None}
        else:
            self.hist_specs = {'weight': None,
                              'age': None,
                              'fitness': None}
            for key in hist_specs:
                self.hist_specs[key] = hist_specs[key]

        np.random.seed(seed)
        if save_name is None:
            self.island_map = Island(map_str=island_map)
        else:
            self.island_map = self.load_simlation(save_name)

        self.plt_speed = plt_speed
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        if img_fmt is None:
            self.img_fmt = 'png'
        else:
            self.img_fmt = img_fmt
        self.add_population(ini_pop)

        self.img_base = img_base
        self.img_fmt = img_fmt
        self.movie_format = movie_format

        if data_name is not None:
            self.data_name = data_name
            filename = f'{data_name}.csv'
            self.file = open(filename, 'a+', newline='')
            self.filewriter = csv.writer(self.file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            # Check if file if empty. 
            # If empty: append column names
            # (Must be a better way to check if the file is empty)
            if os.stat(filename).st_size == 0: 
                self.filewriter.writerow(["Year", "Herbivores", "Carnivores"])
        else:
            self.data_name = None

    @staticmethod
    def set_animal_parameters(species, params):
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

    def simulate(self, num_years, vis_years=1, img_years=None, status_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        viz = Viz(island=self.island_map,
                  num_years=num_years,
                  ymax_animals=self.ymax_animals,
                  cmax_animals=self.cmax_animals,
                  weight_specs=self.hist_specs['weight'],
                  age_specs=self.hist_specs['age'],
                  fitness_specs=self.hist_specs['fitness'],
                  img_base=self.img_base,
                  img_fmt=self.img_fmt)

        # TODO fix map.map.map.map
        for year in range(num_years):
            print(f'Year {year}: ')
            num_herb = self.num_animals_per_species["Herbivore"]
            num_carn = self.num_animals_per_species["Carnivore"]

            # Append animal data to number counter for plotting
            self.island_map.num_herbivores_data.append(num_herb)
            self.island_map.num_carnivores_data.append(num_carn)


            viz.update_data(self.island_map, num_herb, num_carn)

            if vis_years is not None:
                if year % vis_years == 0:
                    viz.update_fig(self.island_map, num_herb, num_carn, self.plt_speed)

            if img_years is not None:
                if year % img_years == 0:
                    viz.save_fig()

            if self.data_name is not None:
                self._save_status(year, num_herb, num_carn)

            self.island_map.new_year()
            self.island_map.year += 1
            print(self.num_animals_per_species)
            # print(self.num_animals_per_species)
            

        plt.close()
        if self.data_name is not None:
            self.file.close()

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

    def save_simulation(self, filename: str) -> None:
        """Method for saving the state of the simulation to a file.
           The file format of the save is .pkl which is a pickle file.
           The state can be loaded using BioSim.load_simulation

        Parameters
        ----------
        filename : str
            Name of the file which the state should be saved to.
            Filename without .pkl
        """
        with open(filename + '.pkl', 'wb') as file:
            pickle.dump(self.island_map, file)

    def load_simlation(self, filename: str) -> Island:
        """Method for loading a pickle file containing the state of a simulation

        Parameters
        ----------
        filename : str
            Full path to the name of the file to be loaded.
            Filename without .pkl

        Returns
        -------
        Island
            Island at the saved state in the simulation
        """
        with open(filename + '.pkl', 'rb') as file:
            return pickle.load(file)

    def make_movie(self):
        """Method for calling ffmpeg in a subprocess to make a movie from images of the simulation

        Raises
        ------
        RuntimeError
            Raises error if anything goes wrong during runtime
        """
        try:
            cmd = f'ffmpeg -r 20 -i img/{self.img_base}_%05d.{self.img_fmt} -b:v 20M {self.img_base}.{self.movie_format}'
            print(cmd)
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as err:
            raise RuntimeError(f"Error creating movie: {err}")

    def _save_status(self, year: int, num_herb: int, num_carn: int):
        """Method for saving the status of the simulation

        Parameters
        ----------
        year : int
            Current year
        num_herb : int
            Number of herbivores in the simulation
        num_carn : int
            Number of carnivores in the simulation
        """
        self.filewriter.writerow([year, num_herb, num_carn])


    @property
    def year(self):
        """Last year simulated."""
        return self.island_map.year

    # TODO: tyr to use these functions inside viz.py instead of doing what we are doing now
    @property
    def num_animals(self) -> int:
        """Total number of animals on island."""
        animal_count = self.num_animals_per_species
        return animal_count["Herbivore"] + animal_count["Carnivore"]

    @property
    def num_animals_per_species(self) -> Dict[str, int]:
        """Number of animals per species in island, as dictionary."""
        animal_count: Dict[str, int] = {"Herbivore": 0,
                                        "Carnivore": 0}  # TODO Refactor with standard values
        for i, row in enumerate(self.island_map.map):
            for j, cell in enumerate(row):
                animal_count["Herbivore"] += cell.n_herbivores
                animal_count["Carnivore"] += cell.n_carnivores

        return animal_count
