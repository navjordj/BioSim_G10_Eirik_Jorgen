from biosim.cells.ocean import Ocean
from biosim.cells.desert import Desert
from biosim.cells.lowland import Lowland
from biosim.cells.highland import Highland


class Island:

    map_params = {'O': Ocean,
                  'D': Desert,
                  'L': Lowland,
                  'H': Highland}

    def __init__(self, map):
        self.map = map

    def make_a_map(self):
        '''
        Makes a map and puts a cell in each position

        :return:
        Full map
        '''
        kart = []
        geo = [list(rader) for rader in
               self.map.replace(" ", "").split("\n")]
        pass
