import unittest
from concurrent.futures import ThreadPoolExecutor
from mocks.connection import Connection
from src.messages.twitch_chat import Chat
from mocks.game.questions_asked import Questions_Asked
from mocks.game.player_scores import Player_Scores
from mocks.silent_log import dont_print
from mocks.spy_log import Spy_Log
from src.messages.terminal import Log
from src.commands import Go

class GoCommandTestCase(unittest.TestCase):
    def test_tuple_returns_the_configured_command_tuple(self):
        subject = Go("mocks/config.txt", "mocks/triviaset.csv", Questions_Asked(), Player_Scores())

        command = subject.tuple()

        self.assertEqual(command[0], "!go")
        self.assertEqual(command[1], subject.run_the_next_trivia_round)
        self.assertEqual(command[2], [ "admin_only" ])

    def test_run_the_next_trivia_round_runs_a_whole_round(self):
        mock_player_scores = Player_Scores()
        s = Go("mocks/config.txt", "mocks/triviaset.csv", Questions_Asked(), mock_player_scores, dont_print)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        s.run_the_next_trivia_round(mock_connection, _message)

        winner = mock_player_scores._round_winners[0][0]
        self.assertTrue(winner in mock_connection._message)

    def go_command_skips_running_the_next_trivia_round_if_theres_an_error(self):
        s = Go("mocks/config.txt", "mocks/bad_triviaset.csv", Questions_Asked(), Player_Scores(), dont_print)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        s.run_the_next_trivia_round(mock_connection, _message)

        self.assertEqual(mock_connection._message, 'No message recieved.')

    def test_go_command_logs_if_theres_an_error(self):
        spy = Spy_Log()
        s = Go("mocks/config.txt", "mocks/bad_triviaset.csv", Questions_Asked(), Player_Scores(), spy.log)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        s.run_the_next_trivia_round(mock_connection, _message)

        self.assertTrue("Ask" in spy._history[0] and "4" in spy._history[0])

    def test_go_command_skips_running_if_another_game_is_in_progress(self):
        spy = Spy_Log()
        mock_player_scores = Player_Scores()
        s = Go("mocks/config.txt", "mocks/triviaset.csv", Questions_Asked(), mock_player_scores, spy.log)

        mock_connection = Connection()
        _message = "irrelevant in this instance"
        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.run_the_next_trivia_round, mock_connection, _message)
            e.submit(s.run_the_next_trivia_round, mock_connection, _message)

        round_start_count = 0
        for message in mock_connection._message_list:
            if mock_player_scores._round_winners[0][0] in message:
                round_start_count += 1
        self.assertEqual(round_start_count, 1)

    def test_go_command_logs_if_another_game_is_in_progress(self):
        spy = Spy_Log()
        mock_player_scores = Player_Scores()
        s = Go("mocks/config.txt", "mocks/triviaset.csv", Questions_Asked(), mock_player_scores, spy.log)

        mock_connection = Connection()
        user = "admiral_akbar"
        command = "!go"
        message = (user, command)
        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.run_the_next_trivia_round, mock_connection, message)
            e.submit(s.run_the_next_trivia_round, mock_connection, message)

        self.assertEqual(spy._history[0], Log.in_progress(user, command))
