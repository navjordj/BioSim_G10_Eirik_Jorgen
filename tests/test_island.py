__author__ = 'Eirik Høyheim, Jørgen Navjord'
__email__ = 'eirihoyh@nmbu.no ,navjordj@gmail.com'

import pytest

from biosim.island import Island  # type: ignore


class Test_island:
    def test_island_start(self) -> None:
        """
        Checks if the island can take in "Water" and can put them in a
        """
        Island('WW\nWW')
        Island('WWWW\nWHLW\nWWLW\nWWWW')
# TODO find out where to test that it start with 1 1
    @pytest.mark.skip(reason='Not implemented yet')
    def test_if_start_with_1_1(self) -> None:
        """
        Tests that the first coordinate of the map is (1, 1)
        """
        testing = Island('WW\nWW')
        if list(testing.map.keys())[0] == (1, 1):
            assert True
        else:
            assert False

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


def test_make_a_map() -> None:
    with pytest.raises(ValueError):
        Island("WWW\nWKW\nWWW")

    def test_if_len_is_not_none(self) -> None:
        k = Island('WWW\nWLW\nWLW\nWWW')
        assert k.row_len is not None
        assert k.column_len is not None
