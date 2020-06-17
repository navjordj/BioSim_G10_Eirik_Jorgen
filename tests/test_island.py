__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import pytest
import numpy as np

from biosim.island import Island  # type: ignore


class Test_island:
    def test_island_start(self) -> None:
        """
        Checks if the island can take in "Water" and can put them in a
        """
        Island('WW\nWW')
        i = Island('WWWW\nWHLW\nWDLW\nWWWW')
        print(i)

    def test_same_len(self) -> None:
        """
        Checks if it raises ValueError when the rows does not have same length
        """
        with pytest.raises(ValueError):
            Island("WWW\nWLLW\nWWW")

    def test_make_map_ready(self) -> None:
        """
        Checks if it raises ValueError when the edges is not water
        """
        with pytest.raises(ValueError):
            Island("WLW\nWLW\nWWW")

        with pytest.raises(ValueError):
            Island("WWW\nLLW\nWWW")

        with pytest.raises(ValueError):
            Island("WWW\nWLW\nWLW")

    def test_make_a_map(self) -> None:
        with pytest.raises(ValueError):
            Island("WWW\nWKW\nWWW")

    def test_if_len_is_not_none(self) -> None:
        k = Island('WWW\nWLW\nWLW\nWWW')
        assert k.row_len is not None
        assert k.column_len is not None

    def test_new_year(self) -> None:
        """
        Check that migration works 
        """
        np.random.seed(1)
        # Should never migrate to a water cell
        for _ in range(1000):
            k = Island('WWW\nWLW\nWWW')
            k.map[1][1].add_animal("Herbivore", 10, 100)
            k.map[1][1].herbivores[0].set_params({"omega": 0}) # Should never die in the new year
            k.new_year()
            assert k.map[1][1].n_herbivores == 1

        np.random.seed(1)
        n_migrated = 1
        for _ in range(1000):
            k = Island('WWWW\nWLLW\nWLLW\nWWWW')
            k.map[1][1].add_animal("Herbivore", age=1, weight=1000)
            k.map[1][1].add_animal("Carnivore", age=1, weight=1000)
            # Probability should be 1/8 to move (0.25*1)/2 (Only two squares possible to move to)
            k.new_year()
            if k.map[1][1].n_herbivores != 1:
                n_migrated += 1
        p_migration = n_migrated/1000
        assert p_migration == pytest.approx(0.125, abs=1e-1) # TODO check if this is right
