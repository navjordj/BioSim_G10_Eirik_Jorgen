from .cell import Lowland
from .animals import Carnivore, Herbivore

from typing import List


class Sim:
    
    def __init__(self, map=None):

        c = Lowland()
        c.add_animals(carnivore=[Carnivore()], herbivore=[Herbivore()])

        self.map: List[Lowland]  = [c]


    def new_year(self):
        c.new_year()




    
