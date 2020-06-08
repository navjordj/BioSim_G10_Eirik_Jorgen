from biosim.simulation import BioSim

ini_herbs = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 6, 'weight': 10} for _ in range(10)]}]
            
ini_carn = [{'loc': (3, 3), 'pop': [{'species': 'Carnivore', 'age': 6, 'weight': 10} for _ in range(3)]}]


kart = "WWW\nWLW\nWWW"


b = BioSim(seed=1, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

b.simulate(1)
