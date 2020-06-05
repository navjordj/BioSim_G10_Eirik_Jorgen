from biosim.simulation import BioSim

ini_herbs = [{'species': 'Herbivore', 'age': 6, 'weight': 10}
             for _ in range(100)]
ini_carn = [{'species': 'Carnivore', 'age': 6, 'weight': 12.5}
            for _ in range(3)]


b = BioSim(seed=1, ini_pop=ini_herbs)
b.add_population(ini_carn)

b.simulate(1)
