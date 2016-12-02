import numpy as np
from matplotlib import pyplot as plt
import lineid_plot

wave = 1240 + np.arange(300) * 0.1
flux = np.random.normal(size=300)

line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

fig, ax = lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1)

b = ax.findobj(match=lambda x: x.get_label() == 'Si II_num_1')[0]
b.set_rotation(0)
b.set_text("Si II$\lambda$1260.42")

line = ax.findobj(match=lambda x: x.get_label() == 'Si II_num_1_line')[0]
line.set_color("red")
line.set_linestyle("-")

plt.show()