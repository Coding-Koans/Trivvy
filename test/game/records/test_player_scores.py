import unittest
from test.test_helpers.file_system import cleanup
from src.game.records.player_scores import Player_Scores as Subject

class PlayerScoresTestCase(unittest.TestCase):
    def test_player_scores_score_adds_new_players_to_the_board(self):
        player = "paul2D2"
        expected = {
            "round_points": 1,
            "game_points": 1,
            "game_wins": 0
        }
        file_name = "mock_players"
        s = Subject(file_name)

        s.score(player)

        cleanup(file_name)
        self.assertEqual(s.scores[player], expected)

    def test_player_scores_score_ups_an_existing_players_score(self):
        player = "paul2D2"
        expected = {
            "round_points": 2,
            "game_points": 2,
            "game_wins": 0
        }
        file_name = "mock_players"
        s = Subject(file_name)

        s.score(player)
        s.score(player)

        cleanup(file_name)
        self.assertEqual(s.scores[player], expected)

    def test_player_scores_score_winner_adds_a_game_win_to_a_player_on_the_board(self):
        players = [ "paul2D2" ]
        expected = {
            players[0]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            }
        }
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(players[0])

        s.score_winners()

        cleanup(file_name)
        self.assertEqual(s.scores, expected)

    def test_player_scores_score_winner_only_adds_a_game_win_to_the_top_player_on_the_board(self):
        players = [ "paul2D2", "the_barron_harkonnen" ]
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(players[0])
        s.score(players[0])
        s.score(players[1])

        s.score_winners()

        cleanup(file_name)
        self.assertEqual(s.scores[players[0]]['game_wins'], 1)
        self.assertEqual(s.scores[players[1]]['game_wins'], 0)

    def test_player_scores_score_winner_only_adds_a_game_win_to_players_on_the_board(self):
        winners = [ "paul2D2", "duncan_idaho" ]
        expected = {
            winners[0]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            }
        }
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(winners[0])

        s.score_winners()

        cleanup(file_name)
        self.assertEqual(s.scores, expected)

    def test_player_scores_score_winner_adds_a_game_win_to__multiple_players_on_the_board(self):
        winners = [ "paul2D2", "gurney" ]
        expected = {
            winners[0]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            },
            winners[1]: {
                "round_points": 1,
                "game_points": 1,
                "game_wins": 1
            }
        }
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(winners[0])
        s.score(winners[1])

        s.score_winners()

        cleanup(file_name)
        self.assertEqual(s.scores, expected)

    def test_player_scores_new_round_clears_all_old_round_scores(self):
        players = [ "duke_leto", "paul2D2" ]
        expected = {
            players[0]: {
                "round_points": 0,
                "game_points": 1,
                "game_wins": 0
            },
            players[1]: {
                "round_points": 0,
                "game_points": 2,
                "game_wins": 1
            }
        }
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(players[0])
        s.score(players[1])
        s.score(players[1])
        s.score_winners()

        s.reset_scores_for_next_round()

        cleanup(file_name)
        self.assertEqual(s.scores, expected)

    def test_player_scores_new_game_clears_all_old_round_and_game_scores(self):
        players = [ "the_great_worm", "paul2D2" ]
        expected = {
            players[0]: {
                "round_points": 0,
                "game_points": 0,
                "game_wins": 1
            },
            players[1]: {
                "round_points": 0,
                "game_points": 0,
                "game_wins": 1
            }
        }
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(players[0])
        s.score(players[1])
        s.score_winners()

        s.reset_scores_for_next_game()

        cleanup(file_name)
        self.assertEqual(s.scores, expected)

    def test_player_scores_round_winners_gives_the_top_3_round_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[3], 5),
            (players[4], 4),
            (players[1], 3)
        ]
        file_name = "mock_players"
        s = Subject(file_name)
        for _ in range(5):
            s.score(players[3])
        for _ in range(4):
            s.score(players[4])
        for _ in range(3):
            s.score(players[1])
        for _ in range(2):
            s.score(players[0])
        s.score(players[2])

        actual = s.round_winners()

        cleanup(file_name)
        self.assertEqual(expected, actual)

    def test_player_scores_game_winners_gives_the_top_3_game_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[3], 5),
            (players[4], 4),
            (players[1], 3)
        ]
        file_name = "mock_players"
        s = Subject(file_name)
        for _ in range(5):
            s.score(players[3])
        for _ in range(4):
            s.score(players[4])
        for _ in range(3):
            s.score(players[1])
        for _ in range(2):
            s.score(players[0])
        s.score(players[2])

        actual = s.game_winners()

        cleanup(file_name)
        self.assertEqual(expected, actual)

    def test_player_scores_top_players_gives_the_top_3_players(self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[3], 5),
            (players[4], 4),
            (players[1], 3)
        ]
        file_name = "mock_players"
        s = Subject(file_name)
        for _ in range(5):
            s.score(players[3])
            s.score_winners()
            s.reset_scores_for_next_game()
        for _ in range(4):
            s.score(players[4])
            s.score_winners()
            s.reset_scores_for_next_game()
        for _ in range(3):
            s.score(players[1])
            s.score_winners()
            s.reset_scores_for_next_game()

        actual = s.top_players()

        cleanup(file_name)
        self.assertEqual(expected, actual)

    def test_player_scores_top_players_gives_first_3_players_to_get_on_the_board_when_there_are_many (self):
        players = [ "paul2D2", "macready_13", "Overdroid", "uberhorse", "aharvey2k" ]
        expected = [
            (players[0], 1),
            (players[1], 1),
            (players[2], 1)
        ]
        file_name = "mock_players"
        s = Subject(file_name)
        for player in players:
            s.score(player)
        s.score_winners()

        actual = s.top_players()

        cleanup(file_name)
        self.assertEqual(expected, actual)

    def test_player_scores_top_players_gives_2_players_when_there_are_only_2 (self):
        players = [ "paul2D2", "macready_13" ]
        expected = [
            (players[1], 2),
            (players[0], 1)
        ]
        file_name = "mock_players"
        s = Subject(file_name)
        for _ in range(2):
            s.score(players[1])
            s.score_winners()
            s.reset_scores_for_next_game()
        s.score(players[0])
        s.score_winners()

        actual = s.top_players()

        cleanup(file_name)
        self.assertEqual(expected, actual)

    def test_player_scores_top_players_gives_the_only_player_whose_played (self):
        players = [ "paul2D2" ]
        expected = [
            (players[0], 1)
        ]
        file_name = "mock_players"
        s = Subject(file_name)
        s.score(players[0])
        s.score_winners()

        actual = s.top_players()

        cleanup(file_name)
        self.assertEqual(expected, actual)

    def test_player_scores_top_players_gives_noting_if_no_one_has_played (self):
        players = [ "paul2D2" ]
        expected = []
        file_name = "mock_players"
        s = Subject(file_name)

        actual = s.top_players()

        cleanup(file_name)
        self.assertEqual(expected, actual)
