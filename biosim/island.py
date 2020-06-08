from .cell import Highland, Water, Lowland, Desert
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


    def __str__(self):
        for i in range(self.row_len):
            for j in range(self.column_len):
                pass
        return ""

    @staticmethod
    def make_map_ready(map_string: str) -> List[List[str]]:
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
        geo = self.make_map_ready(string_map)

        self.row_len = len(geo)
        self.column_len = len(geo[0])

        full_map = [[None]*self.column_len]*self.row_len

        for i, row in enumerate(geo):
            for j, cell in enumerate(row):
                print((i, j), ": ", cell)
                full_map[j][i] = cell
                print(full_map)
        #print(full_map)