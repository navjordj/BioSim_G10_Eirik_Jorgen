.. Biosim Group 10 June 2020 documentation master file, created by
   sphinx-quickstart on Wed Jun 17 13:01:03 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Group 10's documentation!
====================================

This is a package for running biologic simulations according to the specifications from PEAP
The package can be ran by using the following commands:

.. code-block:: python

   from biosim.simulation import BioSim
   ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(50)]}]         
   ini_carn = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(50)]}]

   island_map = """\
                  WWW
                  WLW
                  WWW"""
   b = BioSim(seed=123, ini_pop=ini_herbs, island_map=island_map)
   b.simulate(num_years=50)

Look in the examples directory for more examples

Below is the documentation for the 4 main classes in the package

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   simulation
   island
   cells
   animals





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
