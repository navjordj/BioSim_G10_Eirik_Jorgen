from .cell import Highland, Water, Lowland, Desert
from typing import List

import random


class Island:
    map_params = {'W': Water,
                  'D': Desert,
                  'L': Lowland,
                  'H': Highland}

    def __init__(self, map_str: str) -> None:
        self.row_len = None
        self.column_len = None
        self.map_str = map_str
        self.map = self.make_a_map(map_str)

        self.year = 0

        self.num_herbivores_data: List[int] = []


    def __str__(self):
        map_str = ""
        for i in range(self.row_len):
            for j in range(self.column_len):

                #TODO Refactor to use map_params
                if type(self.map[i][j]) == Water:
                    map_str += 'W'
                else:
                    map_str += "L"
            map_str += "\n"
        return map_str

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
        # TODO make a list comp with None instead of using geo
        for i, row in enumerate(geo):
            for j, cell in enumerate(row):
                if cell not in self.map_params.keys():
                    raise ValueError(f'{cell} is not a valid landscape')
                geo[i][j] = self.map_params[cell]()

        return geo


    def migration(self):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):

                for herbi in cell.herbivores:
                    if herbi.will_migrate():
                        adj_cells: List[Highland, Lowland, Water, Desert] = [self.map[i-1][j], self.map[i+1][j], self.map[i][j-1], self.map[i][j+1]]
                        cell_destination = random.choice(adj_cells)
                        if type(cell_destination) != Water:
                            cell_destination.add_animal("Herbivore", herbi.age, herbi.weight)
                            cell.remove_animal(herbi)
                            # print(f'Migrated from {type(cell).__name__} {(i, j)} to {type(cell_destination).__name__}')
                        else:
                            continue

                for carni in cell.carnivores:
                    if carni.will_migrate():
                        adj_cells: List[Highland, Lowland, Water, Desert] = [self.map[i-1][j], self.map[i+1][j], self.map[i][j-1], self.map[i][j+1]]
                        cell_destination = random.choice(adj_cells)
                        if type(cell_destination) != Water:
                            cell_destination.add_animal("Carnivore", carni.age, carni.weight)
                            cell.remove_animal(carni)
                            # print(f'Migrated from {(i, j)} to {cell_destination}')
                        else:
                            continue

