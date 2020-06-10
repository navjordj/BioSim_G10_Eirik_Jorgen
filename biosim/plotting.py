import matplotlib.pyplot as plt
import numpy as np

def plot_map(island):

    rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                'L': (0.0, 0.6, 0.0),  # dark green
                'H': (0.5, 1.0, 0.5),  # light green
                'D': (1.0, 1.0, 0.5)}  # light yellow

    map_rgb = []
    for row in island.map_str.splitlines():
        map_rgb.append([rgb_value[elm] for elm in row])

    print(map_rgb)

    

    fig = plt.figure()

    axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
    axim.imshow(map_rgb)
    axim.set_xticks(range(len(map_rgb[0])))
    axim.set_xticklabels(range(1, 1 + len(map_rgb[0])))
    axim.set_yticks(range(len(map_rgb)))
    axim.set_yticklabels(range(1, 1 + len(map_rgb)))

    axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
    axlg.axis('off')
    for ix, name in enumerate(('Water', 'Lowland',
                            'Highland', 'Desert')):
        axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                    edgecolor='none',
                                    facecolor=rgb_value[name[0]]))
        axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    plt.show()

def plot_hist():


    def update(n_steps):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, n_steps)
        ax.set_ylim(0, 1)

        line = ax.plot(np.arange(n_steps),
                    np.full(n_steps, np.nan), 'b-')[0]

        for n in range(n_steps):
            ydata = line.get_ydata()
            ydata[n] = np.random.random()
            line.set_ydata(ydata)
            plt.pause(1e-6)
