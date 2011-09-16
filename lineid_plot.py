"""Plot spectral line identifications."""
from __future__ import division, print_function
import numpy as np
from matplotlib import pyplot as plt


def _convert_to_array(x, size, name):
    try:
        l = len(x)
        if l != size:
            raise ValueError(
                "{0} must be scalar or of length {1}".format(
                    name, size))
    except TypeError:
        # Only one item
        xa = np.array([x] * size)
    else:
        xa = np.array(x)

    return xa


def get_line_flux(line_wave, wave, flux, **kwargs):
    return np.interp(line_wave, wave, flux, **kwargs)


def get_box_loc(fig, ax, line_wave, arrow_tip, box_axes_space):
    # Plot boxes in their original x position, at a height given by the
    # key word box_axes_spacing above the top edge of Axes. The default
    # is set to 0.06. This is in figure fraction so that the spacing
    # doesn't depend on the data y range.
    box_loc = []
    fig_inv_trans = fig.transFigure.inverted()
    for w, a in zip(line_wave, arrow_tip):
        # Convert position of tip of arrow, which is equal to arrow_tip
        # to figure coordinates, add the space between top edge and
        # text box in figure fraction. Then convert the text box
        # position back to Axes coordinates.
        display_coords = ax.transData.transform((w, a))
        figure_coords = fig_inv_trans.transform(display_coords)
        figure_coords[1] += box_axes_space
        display_coords = fig.transFigure.transform(figure_coords)
        ax_coords = ax.transData.inverted().transform(display_coords)
        box_loc.append(ax_coords)

    return box_loc


def adjust_boxes(line_wave, box_widths, left_edge, right_edge,
                 adjust_factor=0.35, factor_decrement=3.0,
                 max_iter=1000):
    # Adjust positions.
    niter = 0
    changed = True
    nlines = len(line_wave)

    wlp = line_wave[:]
    while changed:
        changed = False
        for i in range(nlines):
            if i > 0:
                diff1 = wlp[i] - wlp[i - 1]
                separation1 = (box_widths[i] + box_widths[i - 1]) / 2.0
            else:
                diff1 = wlp[i] - left_edge + box_widths[i] * 1.01
                separation1 = box_widths[i]
            if i < nlines - 2:
                diff2 = wlp[i + 1] - wlp[i]
                separation2 = (box_widths[i] + box_widths[i + 1]) / 2.0
            else:
                diff2 = right_edge + box_widths[i] * 1.01 - wlp[i]
                separation2 = box_widths[i]

            if diff1 < separation1 or diff2 < separation2:
                if wlp[i] == left_edge: diff1 = 0
                if wlp[i] == right_edge: diff2 = 0
                if diff2 > diff1:
                    wlp[i] = wlp[i] + separation2 * adjust_factor
                    wlp[i] = wlp[i] if wlp[i] < right_edge else \
                        right_edge
                else:
                    wlp[i] = wlp[i] - separation1 * adjust_factor
                    wlp[i] = wlp[i] if wlp[i] > left_edge else \
                        left_edge
                changed = True
            niter += 1
        if niter == max_iter * 0.75: adjust_factor /= factor_decrement
        if niter >= max_iter: break

    return wlp, changed, niter


def prepare_axes(wave, flux, fig=None, ax_lower=(0.1, 0.1),
                 ax_dim=(0.85, 0.65)):
    # Axes location in figure.
    if not fig:
        fig = plt.figure(1)
    ax = fig.add_axes([ax_lower[0], ax_lower[1], ax_dim[0], ax_dim[1]])
    ax.plot(wave, flux)
    return fig, ax


def plot_line_ids(wave, flux, line_wave, line_label1, label1_size=None,
                  extend=True, **kwargs):
    wave = np.array(wave)
    flux = np.array(flux)
    line_wave = np.array(line_wave)
    line_label1 = np.array(line_label1)

    nlines = len(line_wave)
    assert nlines == len(line_label1), "Each line must have a label."

    if label1_size == None:
        label1_size = np.array([12] * nlines)
    label1_size = _convert_to_array(label1_size, nlines, "lable1_size")

    extend = _convert_to_array(extend, nlines, "extend")

    # Sort.
    indx = np.argsort(wave)
    wave[:] = wave[indx]
    flux[:] = flux[indx]
    indx = np.argsort(line_wave)
    line_wave[:] = line_wave[indx]
    line_label1[:] = line_label1[indx]
    label1_size[:] = label1_size[indx]

    # Flux at the line wavelengths.
    line_flux = get_line_flux(line_wave, wave, flux)

    # Figure and Axes. If Axes is given then use it. If not, create
    # figure, if not given, and add Axes to it using a default
    # layout. Also plot the data in the Axes.
    ax = kwargs.get("ax", None)
    if not ax:
        fig = kwargs.get("fig", None)
        fig, ax = prepare_axes(wave, flux, fig)
    else:
        fig = ax.figure

    # Find location of the tip of the arrow. Either the top edge of the
    # Axes or the given data coordinates.
    ax_bounds = ax.get_ybound()
    arrow_tip = kwargs.get("arrow_tip", ax_bounds[1])
    arrow_tip = _convert_to_array(arrow_tip, nlines, "arrow_tip")

    # The height of the box from the arrow tip. Either given heights in
    # data coordiantes or use the box_axes_space in figure
    # fraction. The latter has a default value and gets used when no
    # box locations are given. Figure coordiantes are used so that
    # the location does not dependent on the data y range.
    box_loc = kwargs.get("box_loc", None)
    if not box_loc:
        box_axes_space = kwargs.get("box_axes_space", 0.06)
        box_loc = get_box_loc(fig, ax, line_wave, arrow_tip, box_axes_space)
    else:
        box_loc = _convert_to_array(box_loc, nlines, "box_loc")
        box_loc = zip(line_wave, box_loc)

    # Draw boxes.
    for i in range(nlines):
        ax.annotate(line_label1[i], xy=(line_wave[i], arrow_tip[i]),
                    xytext=(box_loc[i][0],
                            box_loc[i][1]),
                    xycoords="data", textcoords="data",
                    rotation=90, horizontalalignment="center",
                    verticalalignment="center",
                    fontsize=label1_size[i],
                    arrowprops=dict(arrowstyle="->"))
        if extend[i]:
            ax.plot([line_wave[i]] * 2, [arrow_tip[i], line_flux[i]], "--")

    # Draw the figure so that get_window_extent() below works.
    fig.canvas.draw()

    # Get annotation boxes and convert their dimensions from display
    # coordinates to data coordinates. Specifically, we want the width
    # in wavelength units.
    ax_inv_trans = ax.transData.inverted()
    box_widths = []  # box width in wavelength units.
    # For each annotation box, transform the bounding box into data
    # coordinates and extract the width.
    for box in ax.texts:
        b_ext = box.get_window_extent()
        box_widths.append(b_ext.transformed(ax_inv_trans).width)

    wlp, niter, changed = adjust_boxes(line_wave, box_widths,
                                       np.min(wave), np.max(wave),
                                       adjust_factor=0.35, max_iter=1000)

    # Move the boxes, to new positions.
    for i in range(nlines):
        box = ax.texts[i]
        box.xytext = (wlp[i], box.xytext[1])

    # Update the figure
    fig.canvas.draw()

    return fig, ax

if __name__ == "__main__":
    wave = 1240 + np.arange(300) * 0.1
    flux = np.random.normal(size=300)
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_flux = np.interp(line_wave, wave, flux)
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
    label1_sizes = np.array([12, 12, 12, 12, 12, 12, 12])
    plot_line_ids(wave, flux, line_wave, line_label1)
    plt.show()
