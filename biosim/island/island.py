from biosim.cells.water import Water
from biosim.cells.desert import Desert
from biosim.cells.lowland import Lowland
from biosim.cells.highland import Highland
from typing import List


class Island:
    map_params = {'W': Water,
                  'D': Desert,
                  'L': Lowland,
                  'H': Highland}

    def __init__(self, map: str) -> None:
        self.row_len = None
        self.column_len = None
        self.map = self.make_a_map(map)


    @staticmethod
    def make_map_ready(map_string: str) -> List[str]:
        geo = [list(rows) for rows in
               map_string.replace(" ", "").split("\n")]

        if not all(len(geo[0]) == len(line) for line in geo[1:]):
            raise ValueError('All rows must be equal length')

        for lines in geo:
            if 'W' not in lines[0] or 'W' not in lines[-1]:
                raise ValueError('Edges must be labeled "W" (Water)')

        for i in range(len(geo[0])):
            if 'W' not in geo[0][i] or 'W' not in geo[-1][i]:
                raise ValueError('Edges must be labeled "W" (Water)')

        return geo

    def make_a_map(self, string_map):
        """
        Makes a map and puts a cell in each position

        :return:
        Full map
        """
        full_map = {}
        geo = self.make_map_ready(string_map)

        self.row_len = len(geo)
        self.column_len = len(geo[0])

        for y, row in enumerate(geo):
            for x, cell in enumerate(row):
                if cell in self.map_params.keys():
                    full_map[(y + 1, x + 1)] = self.map_params[cell]
                else:
                    raise ValueError(
                        f'All letters must be uppercase, and all'
                        f'letters must be in '
                        f'{self.map_params.keys()}')

        return full_map
