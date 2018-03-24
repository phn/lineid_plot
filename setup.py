"""Lineid_plot setup.py."""
import os
from setuptools import setup, find_packages

# Read version.py
__version__ = None
curdir = os.path.dirname(__file__)
with open(os.path.join(curdir, 'lineid_plot', 'version.py')) as f:
    exec(f.read())

setup(
    name="lineid_plot",
    version=__version__,
    description="Automatic placement of labels in a plot.",
    license='BSD',
    author="Prasanth Nair",
    author_email="prasanthhn@gmail.com",
    url='https://github.com/phn/lineid_plot',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
