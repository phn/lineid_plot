"""Some tests for lineid_plot."""
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import pytest

import lineid_plot

RFLUX = np.random.RandomState(seed=123).normal(size=300)


def test_unique_labels():
    """Make sure we can create unique labels."""
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
    x = ['N V', 'Si II_num_1', 'Si II_num_2', 'Si II_num_3', 'Si II_num_4',
         'Si II_num_5', 'Si II_num_6']
    assert lineid_plot.unique_labels(line_label1) == x


@pytest.mark.mpl_image_compare
def test_minimal_plot():
    """Test a minimal plot."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX

    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1)

    return fig


@pytest.mark.mpl_image_compare
def test_no_line_from_annotation_to_flux():
    """Must create plot with no line from annotation to flux point."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX

    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, extend=False)
    return fig


@pytest.mark.mpl_image_compare
def test_multi_plot_user_axes():
    """User can supply custom axes."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig = plt.figure()

    # First Axes
    ax = fig.add_axes([0.1, 0.06, 0.85, 0.35])
    ax.plot(wave, flux)

    # Pass the Axes instance to the plot_line_ids function.
    lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, ax=ax)

    # Second Axes
    ax1 = fig.add_axes([0.1, 0.55, 0.85, 0.35])
    ax1.plot(wave, flux)

    # Pass the Axes instance to the plot_line_ids function.
    lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, ax=ax1)

    return fig


@pytest.mark.mpl_image_compare
def test_annotate_kwargs_and_plot_kwargs():
    """User can supply custom annotate and plot kwargs."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX

    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    ak = lineid_plot.initial_annotate_kwargs()
    ak['arrowprops']['arrowstyle'] = "->"

    pk = lineid_plot.initial_plot_kwargs()
    pk['color'] = "red"

    fig, ax = lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1, annotate_kwargs=ak, plot_kwargs=pk)

    return fig


@pytest.mark.mpl_image_compare
def test_customize_box_and_line():
    """User can change box and line aspects after plotting."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX

    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1)

    b = ax.findobj(match=lambda x: x.get_label() == 'Si II_num_1')[0]
    b.set_rotation(0)
    b.set_text("Si II$\lambda$1260.42")

    line = ax.findobj(match=lambda x: x.get_label() == 'Si II_num_1_line')[0]
    line.set_color("red")
    line.set_linestyle("-")

    return fig


@pytest.mark.mpl_image_compare
def test_small_change_to_y_loc_of_label():
    """User can make small changes to y_loc_of_label."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1,
        box_axes_space=0.08)

    return fig


@pytest.mark.mpl_image_compare
def test_custom_y_loc_for_annotation_point():
    """User cna supply custom y_loc for annotation point."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wave, flux)
    ax.axis([1240, 1270, -3, 5])
    lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, arrow_tip=3.3, ax=ax)

    return fig


@pytest.mark.mpl_image_compare
def test_custom_y_loc_for_annotation_point_each_label_sep_loc():
    """User can specific y_loc for each label."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wave, flux)
    ax.axis([1240, 1270, -3, 5])

    arrow_tips = [3.3, 3.3, 3.3, 3.4, 3.5, 3.4, 3.3]
    lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1, arrow_tip=arrow_tips, ax=ax)

    return fig


@pytest.mark.mpl_image_compare
def test_custom_y_loc_for_label_boxes():
    """User can specify y_loc for label box."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wave, flux)
    ax.axis([1240, 1270, -3, 5])
    lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1, arrow_tip=3.3, ax=ax, box_loc=4.3)

    return fig


@pytest.mark.mpl_image_compare
def test_custom_y_loc_for_label_boxes_each_box_sep_loc():
    """User can specify y_loc for each box."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wave, flux)
    ax.axis([1240, 1270, -3, 5])

    arrow_tips = [3.3, 3.3, 3.3, 3.4, 3.5, 3.4, 3.3]
    box_loc = [4.3, 4.3, 4.3, 4.4, 4.5, 4.4, 4.3]
    lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1,
        arrow_tip=arrow_tips, box_loc=box_loc, ax=ax)

    return fig


@pytest.mark.mpl_image_compare
def test_access_a_specific_label():
    """User can access each box and line using label."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(wave, flux)
    ax.axis([1240, 1270, -3, 5])

    arrow_tips = [3.3, 3.3, 3.3, 3.4, 3.5, 3.4, 3.3]
    box_loc = [4.3, 4.3, 4.3, 4.4, 4.5, 4.4, 4.3]
    lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1,
        arrow_tip=arrow_tips, box_loc=box_loc, ax=ax)

    a = ax.findobj(mpl.text.Annotation)
    for i in a:
        if i.get_label() == "Si II_num_4":
            i.set_visible(False)

    a = ax.findobj(mpl.lines.Line2D)
    for i in a:
        if i.get_label() == "Si II_num_4_line":
            i.set_visible(False)

    return fig


@pytest.mark.mpl_image_compare
def test_max_iter_small():
    """User can specify small max_iter."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, max_iter=10)

    return fig


@pytest.mark.mpl_image_compare
def test_max_iter_large():
    """User can specify large max_iter."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, max_iter=300)

    return fig


def test_dont_add_label_to_artists():
    """User can choose to not add labels to artists."""
    wave = 1240 + np.arange(300) * 0.1
    flux = RFLUX
    line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
    line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

    fig, ax = lineid_plot.plot_line_ids(
        wave, flux, line_wave, line_label1, max_iter=300, add_label_to_artists=False
    )

    labels = lineid_plot.unique_labels(line_label1)
    for label in labels:
        assert fig.findobj(match=lambda x: x.get_label() == label) == []
        assert fig.findobj(match=lambda x: x.get_label() == label + "_line") == []
