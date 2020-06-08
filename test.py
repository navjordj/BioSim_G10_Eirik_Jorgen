from biosim.simulation import BioSim

ini_herbs = [{'species': 'Herbivore', 'age': 6, 'weight': None}
             for _ in range(10)]
ini_carn = [{'species': 'Carnivore', 'age': 6, 'weight': None}
            for _ in range(1)]


kart = "WWW\nWLW\nWWW"


b = BioSim(seed=1, ini_pop=ini_herbs, island_map=kart)
b.add_population(ini_carn)

# b.simulate(100)
