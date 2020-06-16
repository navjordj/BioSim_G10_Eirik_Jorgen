import matplotlib.pyplot as plt
import numpy as np
from typing import Dict


class Viz:

    def __init__(self, island,
                 num_years,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt='png'):

        self.y_max_animals = ymax_animals
        self.cmax_animals = cmax_animals

        # save figure params...
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_num = 0

        self.num_years = num_years

        self.figure = None
        self.island_map_ax = None
        self.grid = None
        self.island_map_img_ax = None
        self.herbivores_heat_map_img_ax = None
        self.carnivores_heat_map_img_ax = None
        self.fitness_histogram_img_ax = None
        self.age_histogram_img_ax = None
        self.weight_histogram_img_ax = None
        self.text_img_ax = None

        self.animals_over_time_ax = None

        self.animals_y_max = 0
        self.y_lim_hist = 0

        self.herbivores_over_time = None
        self.carnivores_over_time = None

        self.herbivores_heat_map = None
        self.carnivores_heat_map = None

        self.colorbar_herb = None
        self.colorbar_carn = None

        self.fitness_herb = None
        self.fitness_carn = None

        self.age_herb = None
        self.age_carn = None

        self.weight_herb = None
        self.weight_carn = None

        self.herbivore_counter = None
        self.carnivore_counter = None

        self._setup_graphics()
        self._draw_map(island)
        self._draw_animals_over_time(island)
        self._draw_herbivores_heat_map(self._make_herbivore_heat_map(island))
        self._draw_carnivores_heat_map(self._make_carnivore_heat_map(island))
        herb, carn = self._get_fitness_animals(island)
        self._draw_fitness_histogram(herb, carn)

    def _setup_graphics(self):
        """Creates subplots."""
        if self.figure is None:
            self.figure = plt.figure(constrained_layout=True, figsize=(5, 2))
            self.grid = self.figure.add_gridspec(3, 24)

        if self.island_map_ax is None:
            self.island_map_ax = self.figure.add_subplot(self.grid[0, :10])
            self.island_map_img_ax = None

        if self.animals_over_time_ax is None:
            self.animals_over_time_ax = self.figure.add_subplot(self.grid[0, 12:])

            self.animals_over_time_ax.set_xlim(self.num_years)
            self.animals_over_time_ax.invert_xaxis()
            self.animals_over_time_ax.grid(axis='y', c='g')

        if self.herbivores_heat_map_img_ax is None:
            self.herbivores_heat_map_img_ax = self.figure.add_subplot(self.grid[1, :10])
            self.herbivores_heat_map_img_ax.set(title='Heat map - herbivores')

        if self.colorbar_herb is None:
            self.colorbar_herb = self.figure.add_subplot(self.grid[1, 9])

        if self.carnivores_heat_map_img_ax is None:
            self.carnivores_heat_map_img_ax = self.figure.add_subplot(self.grid[1, 12:])
            self.carnivores_heat_map_img_ax.set(title='Heat map - carnivores')

        if self.colorbar_carn is None:
            self.colorbar_carn = self.figure.add_subplot(self.grid[1, -2])

        if self.text_img_ax is None:
            self.text_img_ax = self.figure.add_subplot(self.grid[0, 10])

        if self.fitness_histogram_img_ax is None:
            self.fitness_histogram_img_ax = self.figure.add_subplot(self.grid[2, :7])
            self.fitness_histogram_img_ax.set(title='Fitness')
            self.fitness_histogram_img_ax.set_ylim(150)
            self.fitness_histogram_img_ax.invert_yaxis()

        if self.age_histogram_img_ax is None:
            self.age_histogram_img_ax = self.figure.add_subplot(self.grid[2, 8:15])
            self.age_histogram_img_ax.set(title='Age')
            self.age_histogram_img_ax.set_ylim(150)
            self.age_histogram_img_ax.invert_yaxis()

        if self.weight_histogram_img_ax is None:
            self.weight_histogram_img_ax = self.figure.add_subplot(self.grid[2, 16:23])
            self.weight_histogram_img_ax.set(title='Weight')
            self.weight_histogram_img_ax.set_ylim(150)
            self.weight_histogram_img_ax.invert_yaxis()

    def _draw_map(self, island):

        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = []
        # TODO see for better solution to write it in
        str_intake = [rows.replace(' ', '') for rows in island.map_str.splitlines()]
        for row in str_intake:
            map_rgb.append([rgb_value[elm] for elm in row])

        self.island_map_img_ax = self.island_map_ax.imshow(map_rgb)

        self.island_map_ax.set_xticks(range(len(map_rgb[0])))
        self.island_map_ax.set_yticks(range(island.row_len))

    def _draw_animals_over_time(self, island):

        self.years = [year for year in range(island.year)]

        self.herbivores_over_time = island.num_herbivores_data.copy()
        self.carnivores_over_time = island.num_carnivores_data.copy()
        print(self.herbivores_over_time)
        for n in range(self.num_years):
            self.herbivores_over_time.append(None)
            self.carnivores_over_time.append(None)
            self.years.append(island.year + n + 1)
        self.years = np.array(self.years)

        self.herbivores_over_time = np.array(self.herbivores_over_time)
        self.carnivores_over_time = np.array(self.carnivores_over_time)
        self.line_herbivore = self.animals_over_time_ax.plot(
            self.years, self.herbivores_over_time, color='b', label='Herbivore'
        )[0]
        self.line_carnivore = self.animals_over_time_ax.plot(
            self.years, self.carnivores_over_time, color='r', label='Carnivore'
        )[0]
        self.animals_over_time_ax.set(xlabel='years', ylabel='Animals')
        self.animals_over_time_ax.legend()

    def _make_herbivore_heat_map(self, island):
        self.herbivores_heat_map = []
        for row in island.map:
            row_list = []
            for cell in row:
                row_list.append(cell.n_herbivores)
            self.herbivores_heat_map.append(row_list)
        return np.array(self.herbivores_heat_map)

    def _draw_herbivores_heat_map(self, heat_map):
        self.herbivores_heat_map_img_ax.set(title='Heat map - herbivores')
        self.herbivores_heat_map = self.herbivores_heat_map_img_ax.imshow(heat_map)
        plt.colorbar(
            self.herbivores_heat_map, cax=self.colorbar_herb
        )

    def _make_carnivore_heat_map(self, island):
        self.carnivores_heat_map = []
        for row in island.map:
            row_list = []
            for cell in row:
                row_list.append(cell.n_carnivores)
            self.carnivores_heat_map.append(row_list)

        return np.array(self.carnivores_heat_map)

    def _draw_carnivores_heat_map(self, heat_map):
        self.carnivores_heat_map_img_ax.set(title='Heat map - carnivores')
        self.carnivores_heat_map = self.carnivores_heat_map_img_ax.imshow(heat_map)
        plt.colorbar(
            self.carnivores_heat_map, self.colorbar_carn
        )

    def _get_fitness_animals(self, island):
        self.fitness_herb = []
        self.fitness_carn = []
        for row in island.map:
            for cell in row:
                for herb in cell.herbivores:
                    self.fitness_herb.append(herb.fitness)
                for carn in cell.carnivores:
                    self.fitness_carn.append(carn.fitness)
        self.fitness_herb = np.array(self.fitness_herb)
        self.fitness_carn = np.array(self.fitness_carn)

        return self.fitness_herb, self.fitness_carn

    def _draw_fitness_histogram(self, fitness_herb, fitness_carn):
        self.fitness_histogram_img_ax.set(title='Fitness')
        self.fitness_histogram_img_ax.invert_yaxis()
        self.hist_line_herb = self.fitness_histogram_img_ax.hist(fitness_herb, color='b',
                                                                 histtype='step')
        self.hist_line_carn = self.fitness_histogram_img_ax.hist(fitness_carn, color='r',
                                                                 histtype='step')

    def _get_age_animals(self, island):
        self.age_herb = []
        self.age_carn = []
        for row in island.map:
            for cell in row:
                for herb in cell.herbivores:
                    self.age_herb.append(herb.age)
                for carn in cell.carnivores:
                    self.age_carn.append(carn.age)
        self.age_herb = np.array(self.age_herb)
        self.age_carn = np.array(self.age_carn)

        return self.age_herb, self.age_carn

    def _draw_age_histogram(self, age_herb, age_carn):
        self.age_histogram_img_ax.set(title='Age')
        self.age_histogram_img_ax.invert_yaxis()
        self.hist_line_herb_age = self.age_histogram_img_ax.hist(age_herb, color='b',
                                                                 histtype='step')
        self.hist_line_carn_age = self.age_histogram_img_ax.hist(age_carn, color='r',
                                                                 histtype='step')

    def _get_weight_animals(self, island):
        self.weight_herb = []
        self.weight_carn = []
        for row in island.map:
            for cell in row:
                for herb in cell.herbivores:
                    self.weight_herb.append(herb.weight)
                for carn in cell.carnivores:
                    self.weight_carn.append(carn.weight)
        self.weight_herb = np.array(self.weight_herb)
        self.weight_carn = np.array(self.weight_carn)

        return self.weight_herb, self.weight_carn

    def _draw_weight_histogram(self, weight_herb, weight_carn):
        self.weight_histogram_img_ax.set(title='Weight')
        self.weight_histogram_img_ax.invert_yaxis()
        self.hist_line_herb_weight = self.weight_histogram_img_ax.hist(weight_herb, color='b',
                                                                       histtype='step')
        self.hist_line_carn_weight = self.weight_histogram_img_ax.hist(weight_carn, color='r',
                                                                       histtype='step')

    def _get_num_animals(self, island):
        self.herbivore_counter = 0
        self.carnivore_counter = 0
        for row in island.map:
            for cell in row:
                self.herbivore_counter += cell.n_herbivores
                self.carnivore_counter += cell.n_carnivores

        return self.herbivore_counter, self.carnivore_counter

    def _draw_text(self, island):
        herb, carn = self._get_num_animals(island)
        self.text_img_ax.axis("off")
        self.text_year = self.text_img_ax.text(0.5, 0.5, f'Years: {island.year}\n'
                                                         f'Herbivores: {herb}\n'
                                                         f'Carnivores: {carn}',
                                               ha='center', wrap=True)

    def update_data(self, island, num_herb, num_carn):
        self.herbivores_over_time[island.year] = num_herb
        self.carnivores_over_time[island.year] = num_carn

    def _update_animals_over_time(self, island, num_herb, num_carn):
        self.line_herbivore.set_ydata(self.herbivores_over_time)

        self.line_carnivore.set_ydata(self.carnivores_over_time)

        # y max will always be the point where one of the animals were the largest
        self.animals_y_max = max(self.animals_y_max, max(num_herb, num_carn))
        self.animals_over_time_ax.set_ylim(self.animals_y_max * 1.1, 0)
        self.animals_over_time_ax.invert_yaxis()

    def _update_heat_maps(self, island):
        self.colorbar_herb.clear()
        self.colorbar_carn.clear()
        self.herbivores_heat_map_img_ax.clear()
        self.carnivores_heat_map_img_ax.clear()
        self._draw_herbivores_heat_map(self._make_herbivore_heat_map(island))
        self._draw_carnivores_heat_map(self._make_carnivore_heat_map(island))
        self.herbivores_heat_map_img_ax.set_xticks(range(island.column_len))
        self.herbivores_heat_map_img_ax.set_yticks(range(island.row_len))
        self.carnivores_heat_map_img_ax.set_xticks(range(island.column_len))
        self.carnivores_heat_map_img_ax.set_yticks(range(island.row_len))

    def _update_fitness_histogram(self, island):
        self.fitness_histogram_img_ax.clear()
        herb, carn = self._get_fitness_animals(island)
        self._draw_fitness_histogram(herb, carn)
        self.y_lim_hist = max((self.carnivores_over_time[island.year],
                               self.herbivores_over_time[
                                   island.year])) * 0.5
        self.fitness_histogram_img_ax.set_ylim(self.y_lim_hist * 1.1, 0)
        self.fitness_histogram_img_ax.invert_yaxis()

    def _update_age_histogram(self, island):
        self.age_histogram_img_ax.clear()
        herb, carn = self._get_age_animals(island)
        self._draw_age_histogram(herb, carn)
        self.age_histogram_img_ax.set_ylim(self.y_lim_hist * 1.1, 0)
        self.age_histogram_img_ax.invert_yaxis()

    def _update_weight_histogram(self, island):
        self.weight_histogram_img_ax.clear()
        herb, carn = self._get_weight_animals(island)
        self._draw_weight_histogram(herb, carn)
        self.weight_histogram_img_ax.set_ylim(self.y_lim_hist * 1.1, 0)
        self.weight_histogram_img_ax.invert_yaxis()

    def _update_text(self, island):
        self.text_img_ax.clear()
        self.island_map_ax.set_title('Island map')
        self._draw_text(island)

    def update_fig(self, island, num_herb, num_carn):
        self._update_animals_over_time(island, num_herb, num_carn)
        self._update_heat_maps(island)
        self._update_fitness_histogram(island)
        self._update_age_histogram(island)
        self._update_weight_histogram(island)
        self._update_text(island)
        plt.pause(1e-2)

    def save_fig(self):
        self.figure.savefig(
            f'{self.img_base}_{self.img_num}.{self.img_fmt}'
        )
        self.img_num += 1
