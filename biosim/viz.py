import matplotlib.pyplot as plt 
import numpy as np


class Viz:

    def __init__(self, island, num_years):

        self.num_years = num_years

        self.figure = None
        self.island_map_ax = None
        self.grid = None
        self.island_map_img_ax = None
        self.herbivores_heat_map_img_ax = None
        self.carnivores_heat_map_img_ax = None

        self.animals_over_time_ax = None

        self.herbivores_over_time = None
        self.carnivores_over_time = None

        self.herbivores_heat_map = None
        self.carnivores_heat_map = None

        self._setup_graphics(island)
        self._draw_map(island)
        self._draw_animals_over_time(island)
        self._draw_herbivores_heat_map(self._make_herbivore_heat_map(island))
        self._draw_carnivores_heat_map(self._make_carnivore_heat_map(island))

    def _setup_graphics(self, island):
        """Creates subplots."""
        if self.figure is None:
            self.figure = plt.figure(constrained_layout=True, figsize=(5, 2))
            self.grid = self.figure.add_gridspec(2, 24)
        
        if self.island_map_ax is None:
            self.island_map_ax = self.figure.add_subplot(self.grid[0, :10])
            self.island_map_img_ax = None

        if self.animals_over_time_ax is None:
            self.animals_over_time_ax = self.figure.add_subplot(self.grid[0, 12:])
            self.animals_over_time_ax.set_ylim(500)
            self.animals_over_time_ax.invert_yaxis()

            self.animals_over_time_ax.set_xlim(self.num_years)
            self.animals_over_time_ax.invert_xaxis()
            self.animals_over_time_ax.grid(axis='y', c='g')

        if self.herbivores_heat_map_img_ax is None:
            self.herbivores_heat_map_img_ax = self.figure.add_subplot(self.grid[1, :10])
            self.herbivores_heat_map_img_ax.set(title='Heat map - herbivores')

        if self.carnivores_heat_map_img_ax is None:
            self.carnivores_heat_map_img_ax = self.figure.add_subplot(self.grid[1, 12:])
            self.carnivores_heat_map_img_ax.set(title='Heat map - carnivores')

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
        self.heat_map_line = self.herbivores_heat_map_img_ax.imshow(heat_map)

    def _make_carnivore_heat_map(self, island):
        self.carnivores_heat_map = []
        for row in island.map:
            row_list = []
            for cell in row:
                row_list.append(cell.n_carnivores)
            self.carnivores_heat_map.append(row_list)

        return np.array(self.carnivores_heat_map)

    def _draw_carnivores_heat_map(self, heat_map):
        self.heat_map_line = self.carnivores_heat_map_img_ax.imshow(heat_map)

    def _update_animals_over_time(self, island):
        self.herbivores_over_time[island.year-1] = island.num_herbivores_data[-1] # last elm
        self.line_herbivore.set_ydata(self.herbivores_over_time)

        self.carnivores_over_time[island.year-1] = island.num_carnivores_data[-1]
        self.line_carnivore.set_ydata(self.carnivores_over_time)

    def _update_heat_maps(self, island):
        self._draw_herbivores_heat_map(self._make_herbivore_heat_map(island))
        self._draw_carnivores_heat_map(self._make_carnivore_heat_map(island))

    # TODO fix so it not only show every other year
    def update_year(self, island):
        self.island_map_ax.set_title(f'Year {island.year}')

    def update_fig(self, island):
        self._update_animals_over_time(island)
        self._update_heat_maps(island)
        self.update_year(island)
        plt.pause(1e-6)
