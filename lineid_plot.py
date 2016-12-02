"""Automatic placement of labels for features in a plot.

Depends on Numpy and Matplotlib.
"""
from __future__ import division, print_function

import warnings
import numpy as np
from matplotlib import pyplot as plt

__version__ = "0.5"
__author__ = "Prasanth Nair"


def _convert_to_array(x, size, name):
    """Check length of array or convert scalar to array.

    Check to see is `x` has the given length `size`. If this is true
    then return Numpy array equivalent of `x`. If not then raise
    ValueError, using `name` as an idnetification. If len(x) returns
    TypeError, then assume it is a scalar and create a Numpy array of
    length `size`. Each item of this array will have the value as `x`.
    """
    try:
        l = len(x)
        if l != size:
            raise ValueError(
                "{0} must be scalar or of length {1}".format(
                    name, size))
    except TypeError:
        # Only one item
        xa = np.array([x] * size)  # Each item is a diff. object.
    else:
        xa = np.array(x)

    return xa


def get_line_flux(line_wave, wave, flux, **kwargs):
    """Interpolated flux at a given wavelength (calls np.interp).
    """
    return np.interp(line_wave, wave, flux, **kwargs)


def unique_labels(line_labels):
    """If a label occurs more than once, add num. as suffix."""
    from collections import defaultdict
    d = defaultdict(int)
    for i in line_labels:
        d[i] += 1
    d = dict((i, k) for i, k in d.items() if k != 1)
    line_labels_u = []
    for lab in reversed(line_labels):
        c = d.get(lab, 0)
        if c >= 1:
            v = lab + "_num_" + str(c)
            d[lab] -= 1
        else:
            v = lab
        line_labels_u.insert(0, v)

    return line_labels_u


def get_box_loc(fig, ax, line_wave, arrow_tip, box_axes_space=0.06):
    """Box loc in data coords, given Fig. coords offset from arrow_tip.

    Parameters
    ----------
    fig: matplotlib Figure artist
        Figure on which the boxes will be placed.
    ax: matplotlib Axes artist
        Axes on which the boxes will be placed.
    arrow_tip: list or array of floats
        Location of tip of arrow, in data coordinates.
    box_axes_space: float
        Vertical space between arrow tip and text box in figure
        coordinates.  Default is 0.06.

    Returns
    -------
    box_loc: list of floats
        Box locations in data coordinates.

    Notes
    -----
    Note that this function is not needed if user provides both arrow
    tip positions and box locations. The use case is when the program
    has to automatically find positions of boxes. In the automated
    plotting case, the arrow tip is set to be the top of the Axes
    (outside this function) and the box locations are determined by
    `box_axes_space`.

    In Matplotlib annotate function, both the arrow tip and the box
    location can be specified. While calculating automatic box
    locations, it is not ideal to use data coordinates to calculate
    box location, since plots will not have a uniform appearance. Given
    locations of arrow tips, and a spacing in figure fraction, this
    function will calculate the box locations in data
    coordinates. Using this boxes can be placed in a uniform manner.

    """
    # Plot boxes in their original x position, at a height given by the
    # key word box_axes_spacing above the arrow tip. The default
    # is set to 0.06. This is in figure fraction so that the spacing
    # doesn't depend on the data y range.
    box_loc = []
    fig_inv_trans = fig.transFigure.inverted()
    for w, a in zip(line_wave, arrow_tip):
        # Convert position of tip of arrow to figure coordinates, add
        # the vertical space between top edge and text box in figure
        # fraction. Convert this text box position back to data
        # coordinates.
        display_coords = ax.transData.transform((w, a))
        figure_coords = fig_inv_trans.transform(display_coords)
        figure_coords[1] += box_axes_space
        display_coords = fig.transFigure.transform(figure_coords)
        ax_coords = ax.transData.inverted().transform(display_coords)
        box_loc.append(ax_coords)

    return box_loc


def adjust_boxes(line_wave, box_widths, left_edge, right_edge,
                 max_iter=1000, adjust_factor=0.35,
                 factor_decrement=3.0, fd_p=0.75):
    """Ajdust given boxes so that they don't overlap.

    Parameters
    ----------
    line_wave: list or array of floats
        Line wave lengths. These are assumed to be the initial y (wave
        length) location of the boxes.
    box_widths: list or array of floats
        Width of box containing labels for each line identification.
    left_edge: float
        Left edge of valid data i.e., wave length minimum.
    right_edge: float
        Right edge of valid data i.e., wave lengths maximum.
    max_iter: int
        Maximum number of iterations to attempt.
    adjust_factor: float
        Gap between boxes are reduced or increased by this factor after
        each iteration.
    factor_decrement: float
        The `adjust_factor` itself if reduced by this factor, after
        certain number of iterations. This is useful for crowded
        regions.
    fd_p: float
        Percentage, given as a fraction between 0 and 1, after which
        adjust_factor must be reduced by a factor of
        `factor_decrement`. Default is set to 0.75.

    Returns
    -------
    wlp, niter, changed: (float, float, float)
        The new y (wave length) location of the text boxes, the number
        of iterations used and a flag to indicated whether any changes to
        the input locations were made or not.

    Notes
    -----
    This is a direct translation of the code in lineid_plot.pro file in
    NASA IDLAstro library.

    Positions are returned either when the boxes no longer overlap or
    when `max_iter` number of iterations are completed. So if there are
    many boxes, there is a possibility that the final box locations
    overlap.

    References
    ----------
    + http://idlastro.gsfc.nasa.gov/ftp/pro/plot/lineid_plot.pro
    + http://idlastro.gsfc.nasa.gov/

    """
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
                if wlp[i] == left_edge:
                    diff1 = 0
                if wlp[i] == right_edge:
                    diff2 = 0
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
        if niter == max_iter * fd_p:
            adjust_factor /= factor_decrement
        if niter >= max_iter:
            break

    return wlp, changed, niter


def prepare_axes(wave, flux, fig=None, ax_lower=(0.1, 0.1),
                 ax_dim=(0.85, 0.65)):
    """Create fig and axes if needed and layout axes in fig."""
    # Axes location in figure.
    if not fig:
        fig = plt.figure()
    ax = fig.add_axes([ax_lower[0], ax_lower[1], ax_dim[0], ax_dim[1]])
    ax.plot(wave, flux)
    return fig, ax


def initial_annotate_kwargs():
    """Default parameters passed to Axes.annotate to create labels."""
    return dict(
        xycoords="data", textcoords="data",
        rotation=90, horizontalalignment="center", verticalalignment="center",
        arrowprops=dict(arrowstyle="-", relpos=(0.5, 0.0))
    )


def initial_plot_kwargs():
    """Default parameters passed to Axes.plot to create line from label into plot."""
    return dict(linestyle="--", color="k",)


def plot_line_ids(wave, flux, line_wave, line_label1, label1_size=None,
                  extend=True, annotate_kwargs={}, plot_kwargs={},
                  **kwargs):
    """Label features with automatic layout of labels.

    Parameters
    ----------
    wave: list or array of floats
        Wave lengths of data.
    flux: list or array of floats
        Flux at each wavelength.
    line_wave: list or array of floats
        Wave length of features to be labelled.
    line_label1: list of strings
        Label text for each line.
    label1_size: list of floats
        Font size in points. If not given the default value in
        Matplotlib is used. This is typically 12.
    extend: boolean or list of boolean values
        For those lines for which this keyword is True, a dashed line
        will be drawn from the tip of the annotation to the flux at the
        line.
    annotate_kwargs : dict
        Keyword arguments to pass to `annotate`, e.g. color.

        Default value is obtained by calling ``initial_annotate_kwargs()``.
    plot_kwargs : dict
        Keyword arguments to pass to `plot`, e.g. color.

        Default value is obtained by calling ``initial_plot_kwargs()``.
    kwargs: key value pairs
        All of these keywords are optional.

        The following keys are recognized:

          ax : Matplotlib Axes
              The Axes in which the labels are to be placed. If not
              given a new Axes is created.
          fig: Matplotlib Figure
              The figure in which the labels are to be placed. If `ax`
              if given then keyword is then ignored. The figure
              associated with `ax` is used. If `fig` and `ax` are not
              given then a new figure is created and an axes is added
              to it.
          arrow_tip: scalar or list of floats
              The location of the annotation point, in data coords. If
              the value is scalar then it is used for all. Default
              value is the upper bound of the Axes, at the time of
              plotting.
          box_loc: scalar or list of floats
              The y axis location of the text label boxes, in data
              units. The default is to place it above the `arrow_tip`
              by `box_axes_space` units in figure fraction length.
          box_axes_space: float
              If no `box_loc` is given then the y position of label
              boxes is set to `arrow_tip` + this many figure fraction
              units. The default is 0.06. This ensures that the label
              layout appearance is independent of the y data range.
          max_iter: int
              Maximum iterations to use. Default is set to 1000.
          add_label_to_artists: boolean
              If True (default is True) then add unique labels to artists, both
              text labels and line extending from text label to spectrum. If
              False then don't add such labels.
    Returns
    -------
    fig, ax: Matplotlib Figure, Matplotlib Axes
        Figure instance on which the labels were placed and the Axes
        instance on which the labels were placed. These can be used for
        further customizations. For example, some labels can be hidden
        by accessing the corresponding `Text` instance form the
        `ax.texts` list.

    Notes
    -----
    + By default the labels are placed along the top of the Axes. The
      annotation point is on the top boundary of the Axes at the y
      location of the line. The y location of the boxes are 0.06 figure
      fraction units above the annotation location. This value can be
      customized using the `box_axes_space` parameter. The value must
      be in figure fractions units. Y location of both labels and
      annotation points can be changed using `arrow_tip` and `box_loc`
      parameters.
    + If `arrow_tip` parameter is given then it is used as the
      annotation point. This can be a list in which case each line can
      have its own annotation point.
    + If `box_loc` is given, then the boxes are placed at this
      position. This too can be a list.
    + `arrow_tip` and `box_loc` are the "y" components of `xy` and
      `xyann` parameters accepted by the `annotate` function in
      Matplotlib.
    + If the `extend` keyword is True then a line is drawn from the
      annotation point to the flux at the line wavelength. The flux is
      calculated by linear interpolation. This parameter can be a list,
      with one value for each line.
    + The maximum iterations to be used can be customized using the
      `max_iter` keyword parameter.
    + add_label_to_artists: Adding labels to artists makes it very easy to get
      reference to an artist using Figure.findobj. But a call to plt.legend()
      will display legend for the lines. Setting add_label_to_artists=False,
      will not add labels to text or lines and solves this issue. We can all
      plt.legend() with artists and labels to only display legends for the
      specified artists.

    """
    wave = np.array(wave)
    flux = np.array(flux)
    line_wave = np.array(line_wave)
    line_label1 = np.array(line_label1)

    nlines = len(line_wave)
    assert nlines == len(line_label1), "Each line must have a label."

    if label1_size is None:
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

    # The y location of boxes from the arrow tips. Either given heights
    # in data coordinates or use `box_axes_space` in figure
    # fraction. The latter has a default value which is used when no
    # box locations are given. Figure coordiantes are used so that the
    # y location does not dependent on the data y range.
    box_loc = kwargs.get("box_loc", None)
    if not box_loc:
        box_axes_space = kwargs.get("box_axes_space", 0.06)
        box_loc = get_box_loc(fig, ax, line_wave, arrow_tip, box_axes_space)
    else:
        box_loc = _convert_to_array(box_loc, nlines, "box_loc")
        box_loc = tuple(zip(line_wave, box_loc))

    # If any labels are repeated add "_num_#" to it. If there are 3 "X"
    # then the first gets "X_num_3". The result is passed as the label
    # parameter of annotate. This makes it easy to find the box
    # corresponding to a label using Figure.findobj. But the downside is that a
    # call to plt.legend() will display legends for the lines (from text to
    # spectrum location). So we don't add the label to artists if the user
    # doesn't want to.
    al = kwargs.get('add_label_to_artists', True)
    label_u = unique_labels(line_label1) if al else [None for _ in line_label1]
    label_u_line = [i + "_line" for i in label_u] if al else label_u

    ak = initial_annotate_kwargs()
    ak.update(annotate_kwargs)
    pk = initial_plot_kwargs()
    pk.update(plot_kwargs)
    # Draw boxes at initial (x, y) location.
    for i in range(nlines):
        ax.annotate(line_label1[i], xy=(line_wave[i], arrow_tip[i]),
                    xytext=(box_loc[i][0],
                            box_loc[i][1]),

                    fontsize=label1_size[i],
                    label=label_u[i],
                    **ak)
        if extend[i]:
            ax.plot([line_wave[i]] * 2, [arrow_tip[i], line_flux[i]],
                    scalex=False, scaley=False,
                    label=label_u_line[i],
                    **pk)

    # Draw the figure so that get_window_extent() below works.
    fig.canvas.draw()

    # Get annotation boxes and convert their dimensions from display
    # coordinates to data coordinates. Specifically, we want the width
    # in wavelength units. For each annotation box, transform the
    # bounding box into data coordinates and extract the width.
    ax_inv_trans = ax.transData.inverted()  # display to data
    box_widths = []  # box width in wavelength units.
    for box in ax.texts:
        b_ext = box.get_window_extent()
        box_widths.append(b_ext.transformed(ax_inv_trans).width)

    # Find final x locations of boxes so that they don't overlap.
    # Function adjust_boxes uses a direct translation of the equivalent
    # code in lineid_plot.pro in IDLASTRO.
    max_iter = kwargs.get('max_iter', 1000)
    adjust_factor = kwargs.get('adjust_factor', 0.35)
    factor_decrement = kwargs.get('factor_decrement', 3.0)
    wlp, niter, changed = adjust_boxes(line_wave, box_widths,
                                       np.min(wave), np.max(wave),
                                       adjust_factor=adjust_factor,
                                       factor_decrement=factor_decrement,
                                       max_iter=max_iter)

    # Redraw the boxes at their new x location.
    for i in range(nlines):
        box = ax.texts[i]
        if hasattr(box, 'xyann'):
            box.xyann = (wlp[i], box.xyann[1])
        elif hasattr(box, 'xytext'):
            box.xytext = (wlp[i], box.xytext[1])
        else:
            warnings.warn("Warning: missing xyann and xytext attributes. "
                          "Your matplotlib version may not be compatible "
                          "with lineid_plot.")

    # Update the figure
    fig.canvas.draw()

    # Return Figure and Axes so that they can be used for further
    # manual customization.
    return fig, ax

if __name__ == "__main__":
    wave = 1240 + np.arange(300) * 0.1
    flux = np.random.normal(size=300)
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_flux = np.interp(line_wave, wave, flux)
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
    label1_size = np.array([12, 12, 12, 12, 12, 12, 12])
    plot_line_ids(wave, flux, line_wave, line_label1, label1_size)
    plt.show()
