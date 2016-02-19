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
ax = fig.add_subplot(111)
ax.plot(wave, flux)
ax.axis([1240, 1270, -3, 5])

arrow_tips = [3.3, 3.3, 3.3, 3.4, 3.5, 3.4, 3.3]
lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1,
  arrow_tip=arrow_tips, ax=ax)

plt.show()