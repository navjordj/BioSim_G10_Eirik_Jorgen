import matplotlib.pyplot as plt 
import numpy as np

class Viz:

    def __init__(self, island, num_years):

        self.num_years = num_years

        self.figure = None
        self.island_map_ax = None
        self.grid = None
        self.island_map_img_ax = None

        self.animals_over_time_ax = None

        self.herbivores_over_time = None


        self._setup_graphics()
        self._draw_map(island)

    def _setup_graphics(self):
        """Creates subplots."""
        if self.figure == None:
            self.figure = plt.figure(constrained_layout=True, figsize=(16, 9))
            self.grid = self.figure.add_gridspec(2, 24)
        
        if self.island_map_ax is None:
            self.island_map_ax = self.figure.add_subplot(self.grid[0, :10])
            self.island_map_ax.set_title("Tittel")
            self.island_map_img_ax = None

        if self.animals_over_time_ax is None:
            self.animals_over_time_ax = self.figure.add_subplot(self.grid[0, 12:])


    def _draw_map(self, island):

        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                'L': (0.0, 0.6, 0.0),  # dark green
                'H': (0.5, 1.0, 0.5),  # light green
                'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = []
        for row in island.map_str.splitlines():
            map_rgb.append([rgb_value[elm] for elm in row])

        self.island_map_img_ax = self.island_map_ax.imshow(map_rgb)

        self.island_map_ax.set_xticks(range(len(map_rgb[0])))


    def _draw_animals_over_time(self, island):

        self.years = [year for year in range(island.year+1)]

        self.herbivores_over_time = island.num_herbivores_data.copy()

        for n in range(self.num_years):
            self.herbivores_over_time.append(None)
            self.years.append(island.year + n + 1)
        self.years = np.array(self.years)
            
        self.herbivores_over_time = np.array(self.herbivores_over_time)


        self.line_herbivore = self.animals_over_time_ax.plot(
            self.years, self.herbivores_over_time, color='b', label='Herbivore'
        )

    def _update_animals_over_time(self, island):
        print(len(island.num_herbivores_data))
        self.herbivores_over_time[2] = island.num_herbivores_data[-1] # last elm

        self.line_herbivore.set_ydata(self.herbivores_over_time)



    def update_fig(self, island):
        self._update_animals_over_time(island)