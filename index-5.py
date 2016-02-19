import numpy as np
from matplotlib import pyplot as plt
import lineid_plot

wave = 1240 + np.arange(300) * 0.1
flux = np.random.normal(size=300)
line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
line_flux = np.interp(line_wave, wave, flux)
line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
label1_sizes = np.array([12, 12, 12, 12, 12, 12, 12])

fig = plt.figure()

# First Axes
ax = fig.add_axes([0.1,0.06, 0.85, 0.35])
ax.plot(wave, flux)

# Pass the Axes instance to the plot_line_ids function.
lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, ax=ax)

# Second Axes
ax1 = fig.add_axes([0.1, 0.55, 0.85, 0.35])
ax1.plot(wave, flux)

# Pass the Axes instance to the plot_line_ids function.
lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, ax=ax1)

plt.show()