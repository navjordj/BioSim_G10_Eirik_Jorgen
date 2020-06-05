from biosim.simulation import BioSim

ini_herbs = [{'species': 'Herbivore', 'age': 6, 'weight': None}
             for _ in range(10)]
ini_carn = [{'species': 'Carnivore', 'age': 6, 'weight': None}
            for _ in range(10)]


b = BioSim(seed=1, ini_pop=ini_herbs)
b.add_population(ini_carn)

b.simulate(10)
