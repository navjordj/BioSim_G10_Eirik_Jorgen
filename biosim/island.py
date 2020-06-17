from .cell import Highland, Water, Lowland, Desert
from typing import List, Any, Union

import random


class Island:
    map_params = {'W': Water,
                  'D': Desert,
                  'L': Lowland,
                  'H': Highland}

    def __init__(self, map_str: str) -> None:
        self.row_len: int = 0
        self.column_len: int = 0
        self.map_str = map_str
        self.map = self.make_a_map(map_str)

        self.year = 0

        self.num_herbivores_data: List[int] = []
        self.num_carnivores_data: List[int] = []

    def __repr__(self) -> str:
        """toString to format how a island should be printed to the console.
        Used for debugging puroposes  

        Returns
        -------
        str
            Formatted string to be printed to the console
        """
        map_str = ""
        for i in range(self.row_len):
            for j in range(self.column_len):

                if type(self.map[i][j]) == Water:
                    map_str += 'W'

                elif type(self.map[i][j]) == Lowland:
                    map_str += 'L'

                elif type(self.map[i][j]) == Highland:
                    map_str += 'H'

                else:
                    map_str += 'D'
            map_str += "\n"
        return map_str

    @staticmethod
    def _prepare_map(map_string: str) -> List[List[str]]:
        """Prepares the input map to be formatted to the proper format

        Parameters
        ----------
        map_string : str
            Unformatted string passed to the island constructor

        Returns
        -------
        List[List[str]]
            List of List of strings properly formatted for make_a_map method

        Raises
        ------
        ValueError
            Raises error if not all rows are of equal length
        ValueError
            Raises error if not all edges are water
        """
        map_string_split = map_string.splitlines()
        map_string_str = [rows.replace(' ', '').replace('\\', '') for rows in map_string_split]
        geo = [list(rows) for rows in map_string_str]
        if not all(len(geo[0]) == len(line) for line in geo[1:]):
            raise ValueError('All rows must be equal length')
        for lines in geo:
            if 'W' not in lines[0] or 'W' not in lines[-1]:
                raise ValueError('Edges must be labeled "W" (Water)')

        for i in range(len(geo[0])):
            if 'W' not in geo[0][i] or 'W' not in geo[-1][i]:
                raise ValueError('Edges must be labeled "W" (Water)')

        return geo

    def make_a_map(self, string_map: str) -> List[List[Union[Highland, Water, Lowland, Desert]]]:
        """Uses prepared map of strings from prepare_map to create the final map.
        The final map is a list of list of cell objects.

        It created the final map in place and only replaces object in the list of lists 

        Parameters
        ----------
        string_map : str
            Input string to be made into a island

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """
        geo = self._prepare_map(string_map)

        self.row_len = len(geo)
        self.column_len = len(geo[0])
        # TODO make a list comp with None instead of using geo
        for i, row in enumerate(geo):
            for j, cell in enumerate(row):
                if cell not in self.map_params.keys():
                    raise ValueError(f'{cell} is not a valid landscape')
                geo[i][j] = self.map_params[cell]()  # type: ignore

        return geo  # type: ignore

    # TODO: tried to make sure that you only migrate once pr year, not sure if necessary
    # TODO: Find a way so it will not migrate more than once pr year.
    #@staticmethod
    def migration(self, cell, adj_cells):

        migrated = 0
        not_migrated = 0
        for i, herbi in enumerate(cell.herbivores):
            if herbi.will_migrate():

                cell_destination = random.choice(adj_cells)
                if cell_destination.allowed_move_to is True:
                    migrated += 1
                    cell_destination.add_animal("Herbivore", herbi.age, herbi.weight)  #TODO: try to put the same animal in, not create new one
                    cell_destination.herbivores[-1].has_migrated = True
                    cell.herbivores[i].alive = False
                else:
                    continue
            else:
                not_migrated += 1


        for i, carni in enumerate(cell.carnivores):
            if carni.will_migrate():
                self.n_migrated += 1

                cell_destination = random.choice(adj_cells)
                if cell_destination.allowed_move_to is True:
                    cell_destination.add_animal("Carnivore", carni.age, carni.weight)
                    cell_destination.carnivores[-1].has_migrated = True
                    cell.carnivores[i].alive = False
                    # print(f'Migrated from {(i, j)} to {cell_destination}')
                else:
                    continue

    def new_year(self) -> None:
        self.n_migrated = 0
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):

                if type(cell) == Lowland or type(cell) == Highland:
                    cell.grow()  # type: ignore
                    cell.eat_herbivore()
                cell.eat_carnivore()

                # Procreation:
                cell.animal_babies()
                # MIGRATION:
                if cell.allowed_move_to is True:
                    adj_cells: List[Union[Highland, Lowland, Water, Desert]] = [self.map[i - 1][j],
                                                                     self.map[i + 1][j],
                                                                     self.map[i][j - 1],
                                                                     self.map[i][j + 1]]
                    self.migration(cell, adj_cells)
                    self.map[i][j].remove_dead_animals()

        for row in self.map:
            for cell in row:
                # Age animals one year:
                cell.new_year()
                # DEATH
                cell.death_animals()
