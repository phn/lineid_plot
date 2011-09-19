#!/usr/bin/env python

from distutils.core import setup

import lineid_plot

version = lineid_plot.__version__

setup(
    name="lineid_plot",
    version=version,
    description="Automatic placement of labels in a plot.",
    license='BSD',
    author="Prasanth Nair",
    author_email="prasanthhn@gmail.com",
    url='https://github.com/phn/lineid_plot',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python',
        ],
    py_modules=["lineid_plot"]
    )
