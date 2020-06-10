import matplotlib.pyplot as plt
import numpy as np


class Simulation():

    def __init__(self):
        self.x = np.range(100)
        self.y = np.full(100, np.nan)

        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._mean_line = None

        self._step = 0
        self._final_step = None
        self._img_ctr = 0

    def simulate(self, num_steps, vis_steps=1):

        self._final_step = self._step + num_steps
        self._setup_graphics()

        while self._step < self._final_step:
            self._update_graphics()

    def _setup_graphics(self):
        """Creates subplots."""

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None

        # Add right subplot for line graph of mean.
        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            self._mean_ax.set_ylim(0, 0.02)

        # needs updating on subsequent calls to simulate()
        self._mean_ax.set_xlim(0, self._final_step + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(np.arange(0, self._final_step),
                                           np.full(self._final_step, np.nan))
            self._mean_line = mean_plot[0]
        else:
            xdata, ydata = self._mean_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_step)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._mean_line.set_data(np.hstack((xdata, xnew)),
                                         np.hstack((ydata, ynew)))

    def _update_system_map(self, sys_map):
        '''Update the 2D-view of the system.'''

        if self._img_axis is not None:
            self._img_axis.set_data(sys_map)
        else:
            self._img_axis = self._map_ax.imshow(sys_map,
                                                 interpolation='nearest',
                                                 vmin=0, vmax=1)
            plt.colorbar(self._img_axis, ax=self._map_ax,
                         orientation='horizontal')

    def _update_mean_graph(self, mean):
        ydata = self._mean_line.get_ydata()
        ydata[self._step] = mean
        self._mean_line.set_ydata(ydata)

    def _update_graphics(self):

        self._update_system_map(self._system.get_status())
        self._update_mean_graph(self._system.mean_value())
        plt.pause(1e-6)


if __name__ == "__main__":
    s = Simulation()
