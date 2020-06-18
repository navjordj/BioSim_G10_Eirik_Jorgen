![Simulation](https://github.com/navjordj/BioSim_G10_Eirik_Jorgen/workflows/Python%20application/badge.svg)

# BioSim Group 10 Eirik and Jørgen

## Installation
```console
pip install git+https://github.com/navjordj/BioSim_G10_Eirik_Jorgen

```

or

```console
git clone https://github.com/navjordj/BioSim_G10_Eirik_Jorgen
cd BioSim_G10_Eirik_Jorgen
pip install .
```


## How to use
``` python
from biosim.simulation import BioSim
   ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(50)]}]         
   ini_carn = [{'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(50)]}]

   island_map = """\
                  WWW
                  WLW
                  WWW"""
   b = BioSim(seed=123, ini_pop=ini_herbs, island_map=island_map)
   b.simulate(num_years=50)
```
More examples are found in examples/


## Description
This package includes software for performing biological simulations in a custom environment. 
The package is implemented according to standards by PEAP.

The main interface is the BioSim class which controls the simulation and all the underlying aspects.

The simulation is performed on an island specified by the user according to PEAP specifications.

The island consists of the following environments:

* Water - W
* Desert - D
* Lowland - L
* Highland - H

The following animals live on the island:
* Herbivores
  * Only eats fodder which is found in Lowland and Highland
* Carnivores
  * Only eats herbivores
