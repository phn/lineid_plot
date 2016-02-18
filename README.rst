Line identification plots using Matplotlib
==========================================

.. _lineid_plot: http://idlastro.gsfc.nasa.gov/ftp/pro/plot/lineid_plot.pro
.. _IDL Astronomy User's Library: http://idlastro.gsfc.nasa.gov/
.. _pip: http://pypi.python.org/pypi/pip 
.. _easy_install: http://packages.python.org/distribute/easy_install.html

Manually labeling features in a crowed plot can be very time
consuming. Functions in this module can be used to automatically place
labels without the labels overlapping each other. This is useful, for
example, in creating plots of spectrum with lines identified with
labels.

Examples illustrating all these features are shown at
http://phn.github.com/lineid_plot . Source for these are included in
the `doc/index.rst` file as embedded code in ``..plot:``
reStructuredText directives.

Installation
============

Use `pip`_ or `easy_install`_::

  $ pip install lineid_plot
  
or::

  $ easy_install lineid_plot


To download the entire repository either clone the repository or use
the *Download* button. To download just the `lineid_plot.py` file,
click on the file and then download the *raw* version.

Examples
========

Detailed examples are provided at http://phn.github.com/lineid_plot .

A basic plot can be created by calling the function
``plot_line_ids()``, and passing labels and x-axis locations of
features.

.. image:: simple_plot.png?raw=true
   :scale: 75%

.. code-block:: python

   >>> import numpy as np
   >>> from matplotlib import pyplot as plt
   >>> import lineid_plot

   >>> wave = 1240 + np.arange(300) * 0.1
   >>> flux = np.random.normal(size=300)

   >>> line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
   >>> line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']

   >>> lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1)
   >>> plt.show()


The ``plot_line_ids()`` function also accepts Axes and/or Figure
instances where labels are to be draw. 

.. image:: multi_axes.png?raw=true
   :scale: 75%

.. code-block:: python

  >>> import numpy as np
  >>> from matplotlib import pyplot as plt
  >>> import lineid_plot
   
  >>> wave = 1240 + np.arange(300) * 0.1
  >>> flux = np.random.normal(size=300)
  >>> line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
  >>> line_flux = np.interp(line_wave, wave, flux)
  >>> line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
  >>> label1_sizes = np.array([12, 12, 12, 12, 12, 12, 12])
   
  >>> fig = plt.figure(1)
  
  >>> ax = fig.add_axes([0.1,0.06, 0.85, 0.35])
  >>> ax.plot(wave, flux)
  >>> lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, ax=ax)

  >>> ax1 = fig.add_axes([0.1, 0.55, 0.85, 0.35])
  >>> ax1.plot(wave, flux)
  >>> lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, ax=ax1)


Each of the boxes and the lines extending to the flux level have their
label property set to a unique value. These can be used to quickly
identify them.

.. code-block:: python

  >>> for i in ax.texts:
     ....:     print i.get_label()
     ....:     
  N V
  Si II_num_1
  Si II_num_2
  Si II_num_3
  Si II_num_4
  Si II_num_5
  Si II_num_6
  >>> for i in ax.lines:
     ....:     print i.get_label()
     ....:     
  _line0
  N V_line
  Si II_num_1_line
  Si II_num_2_line
  Si II_num_3_line
  Si II_num_4_line
  Si II_num_5_line
  Si II_num_6_line


The label ``_line0`` corresponds to the data plot and was assigned by
Matplotlib.

Details
=======

The placements are calculated using a simple, iterative algorithm
adapted from the procedure `lineid_plot`_ in the NASA `IDL Astronomy
User's Library`_. Matplotlib makes most of the other computations such
as extracting width of label boxes, re-positioning them etc., very
easy.

The main function in the module is ``plot_line_ids()``. Labeled plots can
be created by passing the x and y coordinates, for example wavelength
and flux, along with the x coordinates of the features and their
labels. The x coordinates are adjusted until the labels, of given size,
do not overlap, or when the iteration limit is reached.

Users can provide the Axes instance or the Figure instance on which
plots are to be made. If an Axes instance is provided, then the data is
not plotted; only the labels are marked. This allows the user to
separate plotting from labeling. For example, the user can create
multiple Axes on a figure and then pass the Axes on which labels are to
be marked. No changes are made to the existing layout. 

The y axis locations of labels and annotation points i.e., arrow tips,
can also be passed to the ``plot_line_ids()`` function. Minor changes can
be passed using the ``box_axes_space`` keyword, where as major changes
can be passed using the ``arrow_tip`` and ``box_loc`` keywords. The former
is in figure fraction units and the latter two are in data
coordinates. The latter two can be specified separately for each
label. This is very useful in crowded regions. These features along
with the ability to pass an Axes instance gives the program a lot of
flexibility.

An extension line from the annotation point to the y data value at the
location of the identification i.e., flux level at the line, is drawn
by default. The flux at the line is calculated using linear
interpolation. This can be turned off using the ``extend`` keyword. This
keyword can be set separately for each feature.

The ``plot_line_ids()`` function will return the Axes and Figure
instances used. Additional customizations, such as manual adjustments
to positions, can be carried out using these references. To easily
identify the labels, each label box and extension lines have their
``label`` property set to a string that depends on the label text
provided. Identifying the Matplotlib objects corresponding to these and
customizing them are made easy by the many features provided by
Matplotlib.

The maximum iterations to use can be supplied using the ``max_iter``
keyword. The adjustments to be made in each iteration and when to
change the adjustment factor can also be supplied. The defaults for
these should be enough for most cases.

License
=======

Released under BSD; see http://www.opensource.org/licenses/bsd-license.php.

Credits
=======

Code here is adapted from `lineid_plot`_ procedure in the 
`IDL Astronomy User's Library`_ (IDLASTRO) IDL code distributed by NASA. 

For comments and suggestions, email to user prasanthhn in the gmail.com domain. 


..  LocalWords:  lineid IDL idlastro gsfc nasa


