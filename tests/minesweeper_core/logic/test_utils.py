import minesweeper_core.logic.utils as utils
from minesweeper_core.data.cell import Cell


class TestUtilFunctions:
    def test_is_alone_cell_success_condition(self) -> None:
        assert utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=False, is_open=False, has_flag=False, neighbour_mines=0
        ))

    def test_is_alone_cell_failure_condition_1(self) -> None:
        assert not utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=True, is_open=False, has_flag=False, neighbour_mines=0
        ))

    def test_is_alone_cell_failure_condition_2(self) -> None:
        assert not utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=False, is_open=True, has_flag=False, neighbour_mines=0
        ))

    def test_is_alone_cell_failure_condition_3(self) -> None:
        assert not utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=False, is_open=False, has_flag=False, neighbour_mines=1
        ))

    def test_is_alone_cell_failure_condition_4(self) -> None:
        assert not utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=True, is_open=True, has_flag=True, neighbour_mines=4
        ))

    def test_is_alone_cell_failure_condition_5(self) -> None:
        assert not utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=True, is_open=False, has_flag=True, neighbour_mines=2
        ))

    def test_is_alone_cell_failure_condition_6(self) -> None:
        assert not utils.is_alone_cell(Cell(
            row=0, column=0, has_mine=False, is_open=True, has_flag=True, neighbour_mines=9
        ))

    def test_has_neighbour_mines_success_condition(self) -> None:
        assert utils.has_neighbour_mines(Cell(
            row=0, column=0, has_mine=False, is_open=False, has_flag=False, neighbour_mines=1
        ))

    def test_has_neighbour_mines_failure_condition_1(self) -> None:
        assert not utils.has_neighbour_mines(Cell(
            row=0, column=0, has_mine=False, is_open=False, has_flag=False, neighbour_mines=0
        ))

    def test_has_neighbour_mines_failure_condition_2(self) -> None:
        assert not utils.has_neighbour_mines(Cell(
            row=0, column=0, has_mine=True, is_open=False, has_flag=False, neighbour_mines=1
        ))

    def test_has_neighbour_mines_failure_condition_3(self) -> None:
        assert not utils.has_neighbour_mines(Cell(
            row=0, column=0, has_mine=False, is_open=True, has_flag=False, neighbour_mines=1
        ))

    def test_has_neighbour_mines_failure_condition_4(self) -> None:
        assert not utils.has_neighbour_mines(Cell(
            row=0, column=0, has_mine=False, is_open=False, has_flag=True, neighbour_mines=1
        ))

    def test_has_neighbour_mines_failure_condition_5(self) -> None:
        assert not utils.has_neighbour_mines(Cell(
            row=0, column=0, has_mine=True, is_open=False, has_flag=True, neighbour_mines=0
        ))

    def test_get_neighbour_coordinates_0_0_4_4_eq_3(self) -> None:
        neighbours_0_0_4_4 = utils.get_neighbour_coordinates((0, 0), 4, 4)
        assert len(neighbours_0_0_4_4) == 3

    def test_get_neighbour_coordinates_0_3_4_4_eq_3(self) -> None:
        neighbours_0_3_4_4 = utils.get_neighbour_coordinates((0, 3), 4, 4)
        assert len(neighbours_0_3_4_4) == 3

    def test_get_neighbour_coordinates_3_0_4_4_eq_3(self) -> None:
        neighbours_3_0_4_4 = utils.get_neighbour_coordinates((3, 0), 4, 4)
        assert len(neighbours_3_0_4_4) == 3

    def test_get_neighbour_coordinates_3_3_4_4_eq_3(self) -> None:
        neighbours_3_3_4_4 = utils.get_neighbour_coordinates((3, 3), 4, 4)
        assert len(neighbours_3_3_4_4) == 3

    def test_get_neighbour_coordinates_1_0_4_4_eq_5(self) -> None:
        neighbours_1_0_4_4 = utils.get_neighbour_coordinates((1, 0), 4, 4)
        assert len(neighbours_1_0_4_4) == 5

    def test_get_neighbour_coordinates_1_1_4_4_eq_8(self) -> None:
        neighbours_1_1_4_4 = utils.get_neighbour_coordinates((1, 1), 4, 4)
        assert len(neighbours_1_1_4_4) == 8
