from biosim.cells import Highland, Water, Lowland, Desert
from typing import List, Union

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
        Used for debugging purpose

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
        geo: list of lists
            each index has a cell object

        Raises
        ------
        ValueError
            can't set an index if it's not in the map_params dictionary
        """
        geo = self._prepare_map(string_map)

        self.row_len = len(geo)
        self.column_len = len(geo[0])

        for i, row in enumerate(geo):
            for j, cell in enumerate(row):
                if cell not in self.map_params.keys():
                    raise ValueError(f'{cell} is not a valid landscape')
                geo[i][j] = self.map_params[cell]()  # type: ignore

        return geo  # type: ignore

    @staticmethod
    def migration(cell, adj_cells):  # TODO: add types
        """
        Static method that runs over all animals in a given cel and checks if they can migrate
        or not. If they can, they will migrate to one of four cells, which are given
        in the adj_cells. If the cell they choose in the adj_cells is water, they will stay in the
        cell. If they are not able to migrate, then they will also stay in their cell.
        Parameters
        ----------
        cell :
            The cell the animals is curently in
        adj_cells :
            Cells that are around the cell we currently are in
        """
        for i, herbi in enumerate(cell.herbivores):
            if herbi.will_migrate():

                cell_destination = random.choice(adj_cells)
                if cell_destination.allowed_move_to:
                    cell_destination.add_animal("Herbivore", herbi.age, herbi.weight)  #TODO: try to put the same animal in, not create new one
                    cell_destination.herbivores[-1].has_migrated = True
                    cell.herbivores[i].alive = False

        for i, carni in enumerate(cell.carnivores):
            if carni.will_migrate():

                cell_destination = random.choice(adj_cells)
                if cell_destination.allowed_move_to:
                    cell_destination.add_animal("Carnivore", carni.age, carni.weight)
                    cell_destination.carnivores[-1].has_migrated = True
                    cell.carnivores[i].alive = False

    def new_year(self) -> None:
        """
        Goes through the new year after The Annual Cycle on Rossumøya, first feeding, then
        procreation, migration, aging, loss of weight and at last death.
        In the first double for-loop, it goes through all cells in the map and grow fodder,
        feeds the animals, start procreation and then migrate.
        In the second double for-loop, it goes through all animals once more to set age,
        update weight and then see if they survives the year or dies of 'natural conditions'
        """
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
