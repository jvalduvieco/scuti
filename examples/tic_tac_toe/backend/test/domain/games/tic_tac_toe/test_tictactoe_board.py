from unittest import TestCase

from domain.games.tic_tac_toe.board import TicTacToeBoard
from domain.games.types import PlayerId


class TestTicTacToeBoard(TestCase):
    def test_can_place_a_mark_in_the_first_row(self):
        board = TicTacToeBoard()
        player_id = PlayerId()
        self.assertEqual(TicTacToeBoard({(1, 2): player_id}), board.place(1, 2, player_id))

    def test_can_place_n_mark(self):
        board = TicTacToeBoard()
        player_id = PlayerId()
        self.assertEqual(TicTacToeBoard({(1, 1): player_id,
                                         (2, 1): player_id}),
                         board.place(1, 1, player_id).place(2, 1, player_id))

    def test_when_there_are_no_free_cells_board_is_full(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 0, player_id).place(0, 1, player_id).place(0, 2, player_id) \
            .place(1, 0, player_id).place(1, 1, player_id).place(1, 2, player_id) \
            .place(2, 0, player_id).place(2, 1, player_id).place(2, 2, player_id)
        self.assertTrue(board.is_full())

    def test_when_there_are_some_marks_and_free_cells_board_is_not_full(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 0, player_id).place(1, 1, player_id).place(0, 2, player_id)
        self.assertFalse(board.is_full())

    def test_finds_the_player_with_three_in_the_first_row(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 0, player_id).place(1, 0, player_id).place(2, 0, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_second_row(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 1, player_id).place(1, 1, player_id).place(2, 1, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_third_row(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 2, player_id).place(1, 2, player_id).place(2, 2, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_first_col(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 0, player_id).place(0, 1, player_id).place(0, 2, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_second_col(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(1, 0, player_id).place(1, 1, player_id).place(1, 2, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_third_col(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(2, 0, player_id).place(2, 1, player_id).place(2, 2, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_left_top_to_bottom_right_diagonal(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(0, 0, player_id).place(1, 1, player_id).place(2, 2, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_finds_the_player_with_three_in_the_right_top_to_bottom_left_diagonal(self):
        player_id = PlayerId()
        board = TicTacToeBoard() \
            .place(2, 0, player_id).place(1, 1, player_id).place(0, 2, player_id)
        self.assertEqual(player_id, board.any_player_has_three_in_a_row())

    def test_can_be_serialized_to_a_list_of_cells_when_empty(self):
        board = TicTacToeBoard()
        self.assertEqual([[None, None, None], [None, None, None], [None, None, None]], board.to_list())

    def test_can_be_serialized_to_a_list_of_cells_when_there_are_some_placed(self):
        player_id = PlayerId()
        board = TicTacToeBoard().place(2, 0, player_id).place(1, 1, player_id).place(0, 2, player_id)
        self.assertEqual([[None, None, player_id],
                          [None, player_id, None],
                          [player_id, None, None]], board.to_list())
