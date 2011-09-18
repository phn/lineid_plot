.. Line Identification Plots documentation master file, created by
   sphinx-quickstart on Sun Sep 18 11:26:57 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Line identification plots with automatic label layout
=====================================================

.. contents::

.. toctree::
   :maxdepth: 2

Manually placing labels in plots of spectrum is cumbersome. This module
attempts to automatically position labels, in such a way that they do
not overlap with each other.

The function `plot_line_ids()` takes several keyword parameters that
can be used to customized the placement of labels. The labels are
generated using the `annotate` function in Matplotlib. The function
returns the Figure and Axes instances used, so that further
customizations can be performed.

Some example are shown below.

Minimal plot with automatic label layout
----------------------------------------

.. plot:: 
   :include-source:

   import numpy as np
   from matplotlib import pyplot as plt
   import lineid_plot
    
   wave = 1240 + np.arange(300) * 0.1
   flux = np.random.normal(size=300)
    
   line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
   line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
    
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1)
    
   plt.show()

Plot without line from annotation point to flux level
-----------------------------------------------------

.. plot:: 
   :include-source:

   import numpy as np
   from matplotlib import pyplot as plt
   import lineid_plot
    
   wave = 1240 + np.arange(300) * 0.1
   flux = np.random.normal(size=300)
    
   line_wave = [1242.80, 1260.42, 1264.74, 1265.00, 1265.2, 1265.3, 1265.35]
   line_label1 = ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
    
   # Set extend=False.
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, extend=False)
    
   plt.show()

Multiple plots using user provided Axes instances
-------------------------------------------------

.. plot::
   :include-source:

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


Custom y axis location for annotation points (arrow tips)
---------------------------------------------------------

Use arrow_tip keyword to alter the annotation point. When assigning
custom y axis locations, it is best to plot the data, set appropriate
range for the Axes and then pass the Axes instance to
`plot_line_ids()`.

.. code-block:: python

   # Use arrow_tip keyword.
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=3.3, ax=ax)

.. plot::

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
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=3.3, ax=ax)
   
   plt.show()

Each label can have its own annotation point.

.. code-block:: python

   arrow_tips = [3.3, 3.3, 3.3, 3.4, 3.5, 3.4, 3.3]
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=arrow_tips, ax=ax)

.. plot::

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


Custom y axis location for label boxes
--------------------------------------

The label boxes can be given a custom y axis location. The value given
is taken as the y coordinate of the center of a box, in data
coordinates. When assigning custom Y locations, it is best to plot the
data, set appropriate range for the Axes and then pass the Axes
instance to `plot_line_ids()`.

.. code-block:: python

   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=3.3, ax=ax, box_loc=4.3)

.. plot::

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
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=3.3, ax=ax, box_loc=4.3)
   
   plt.show()


Each box can be assigned a separate Y box location.

.. code-block:: python

   arrow_tips = [3.3, 3.3, 3.3, 3.4, 3.5, 3.4, 3.3]
   box_loc = [4.3, 4.3, 4.3, 4.4, 4.5, 4.4, 4.3]
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=arrow_tips, box_loc=box_loc, ax=ax)

.. plot::

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
   box_loc = [4.3, 4.3, 4.3, 4.4, 4.5, 4.4, 4.3]
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=arrow_tips, box_loc=box_loc, ax=ax)
   
   plt.show()


Accessing a specific label
--------------------------

Each box has a property named `label`. These are identical to the input
labels, except when there are duplicated. The duplicate texts are given
a numeric suffix, based on the order in which the duplicates occur in
the input. These are generated using the `unique_labels` function. 

.. code-block:: python

  >>> line_label1
  ['N V', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II', 'Si II']
  >>> lineid_plot.unique_labels(line_label1)
  ['N V',
   'Si II_num_1',
   'Si II_num_2',
   'Si II_num_3',
   'Si II_num_4',
   'Si II_num_5',
   'Si II_num_6']

Each line extending from the annotation point to the flux level, is
also assigned a label properties. The value is the above label
property suffixed with "_line".

Matplotlib ``Figure`` and ``Axes`` instances have a method
``findobj()`` which can be used to find objects in it, that satisfy
certain conditions. For example, all ``Annotation`` objects. It will
accept a function, and any object that will cause this function to
return True, will be returned by ``findobj()``.

In the following one of the "Si II" boxes and line extending to the
flux level are made invisible.

.. plot::
   :include-source:

   import numpy as np
   from matplotlib import pyplot as plt
   import matplotlib as mpl
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
   box_loc = [4.3, 4.3, 4.3, 4.4, 4.5, 4.4, 4.3]
   lineid_plot.plot_line_ids(wave, flux, line_wave, line_label1, 
     arrow_tip=arrow_tips, box_loc=box_loc, ax=ax)

   a = ax.findobj(mpl.text.Annotation)
   for i in a:
       if i.get_label() == "Si II_num_4":
          i.set_visible(False)

   a = ax.findobj(mpl.lines.Line2D)
   for i in a:
       if i.get_label() == "Si II_num_4_line":
          i.set_visible(False)

   plt.show()


.. Indices and tables
.. ==================
..  
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

