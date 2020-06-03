from biosim.cells.ocean import Ocean
from biosim.cells.desert import Desert
from biosim.cells.lowland import Lowland
from biosim.cells.highland import Highland


class Island:

    map_params = {'W': Ocean,
                  'D': Desert,
                  'L': Lowland,
                  'H': Highland}

    def __init__(self, map):
        self.map = self.make_a_map(map)
        self.row_len = None
        self.column_len = None

    def make_a_map(self, string_map):
        '''
        Makes a map and puts a cell in each position

        :return:
        Full map
        '''
        full_map = {}
        geo = [list(rows) for rows in
               string_map.replace(" ", "").split("\n")]

        if not all(len(geo[0]) == len(line) for line in geo[1:]):
            raise ValueError('All rows must be equal')

        else:

            self.row_len = len(geo)
            self.column_len = len(geo[0])

            for x, row in enumerate(geo):
                for y, cell in enumerate(row):
                    if cell in self.map_params.keys():
                        full_map[(x+1, y+1)] = self.map_params[cell]
                    else:
                        raise ValueError(f'All letters must be uppercase, and all'
                                         f'letters must be in '
                                         f'{self.map_params.keys()}')

            return full_map

