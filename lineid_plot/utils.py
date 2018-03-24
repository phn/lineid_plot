"""Some utility functions."""
import matplotlib as mpl
import lineid_plot
from lineid_plot import unique_labels


def get_labels(labels):
    """Create unique labels."""
    label_u = unique_labels(labels)
    label_u_line = [i + "_line" for i in label_u]
    return label_u, label_u_line


def get_boxes_and_lines(ax, labels):
    """Get boxes and lines using labels as id."""
    labels_u, labels_u_line = get_labels(labels)
    boxes = ax.findobj(mpl.text.Annotation)
    lines = ax.findobj(mpl.lines.Line2D)
    lineid_boxes = []
    lineid_lines = []

    for box in boxes:
        l = box.get_label()
        try:
            loc = labels_u.index(l)
        except ValueError:
            # this box is either one not added by lineidplot or has no label.
            continue
        lineid_boxes.append(box)

    for line in lines:
        l = line.get_label()
        try:
            loc = labels_u_line.index(l)
        except ValueError:
            # this line is either one not added by lineidplot or has no label.
            continue
        lineid_lines.append(line)

    return lineid_boxes, lineid_lines


def color_text_boxes(ax, labels, colors, color_arrow=True):
    """Color text boxes.

    Instead of this function, one can pass annotate_kwargs and plot_kwargs to
    plot_line_ids function.
    """
    assert len(labels) == len(colors), \
        "Equal no. of colors and lables must be given"
    boxes = ax.findobj(mpl.text.Annotation)
    box_labels = lineid_plot.unique_labels(labels)
    for box in boxes:
        l = box.get_label()
        try:
            loc = box_labels.index(l)
        except ValueError:
            continue  # No changes for this box
        box.set_color(colors[loc])
        if color_arrow:
            box.arrow_patch.set_color(colors[loc])

    ax.figure.canvas.draw()


def color_lines(ax, labels, colors):
    """Color lines.

    Instead of this function, one can pass annotate_kwargs and plot_kwargs to
    plot_line_ids function.
    """
    assert len(labels) == len(colors), \
        "Equal no. of colors and lables must be given"
    lines = ax.findobj(mpl.lines.Line2D)
    line_labels = [i + "_line" for i in lineid_plot.unique_labels(labels)]
    for line in lines:
        l = line.get_label()
        try:
            loc = line_labels.index(l)
        except ValueError:
            continue  # No changes for this line
        line.set_color(colors[loc])

    ax.figure.canvas.draw()
