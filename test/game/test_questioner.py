import unittest
import time
from concurrent.futures import ThreadPoolExecutor
from mocks.connection import Connection
from mocks.game.questions_asked import Questions_Asked
from mocks.game.player_scores import Player_Scores
from mocks.game.timer import Timer
from src.messages import Chat
from src.game.questioner import Questioner as Subject



class QuestionerTestCase(unittest.TestCase):
    def test_questioner_knows_itself_and_expects_strings_as_input(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        self.assertEqual(s.ask, "What's a Diorama?")
        self.assertEqual(type(s.ask), str)
        self.assertEqual(type(s.ask), str)


    def test_questioner_doesnt_care_if_there_are_extra_fields(self):
        question = {
            'Round': 1,
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!",
            'Answer2': 'D\'oh!'
        }
        Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())

    def test_questioner_gives_its_ask(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        subject = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        self.assertEqual(subject.ask, "What's a Diorama?")

    def test_questioner_identifies_an_exact_correct_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        participant_answer = "OMG Han! Chewie! They're all here!"
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, True)

    def test_questioner_identifies_an_incorrect_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        participant_answer = "I don't know, some kind of goblin-man."
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, False)

    def test_questioner_identifies_a_correct_answer_with_extra_whitespace(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        participant_answer = " \t \rOMG Han! Chewie! They're all here!\r \n "
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, True)

    def test_questioner_identifies_a_correct_answer_ignoring_internal_whitespace(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        participant_answer = " \t \rOMGHan!   Chewie! \t They're all here!\r \n "
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, True)

    def test_questioner_identifies_a_correct_answer_ignoring_case(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        participant_answer = "OmG hAn! CheWIe! theY're all hEre!"
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, True)

    def test_questioner_identifies_a_correct_answer_inside_a_message(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        participant_answer = "I would say OMG Han! Chewie! They're all here! what do you think?"
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, True)

    def test_questioner_identifies_a_correct_answer_even_with_garbage_characters_interleaved(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        participant_answer = "O!M@G#H$a%n^?&C*(h)e_w-i+e=!{T}[h]e|y'r\\e:a;l\"l'<h>e,r.e/"
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        actual = s.check_answer(participant_answer)
        self.assertEqual(actual, True)

    def test_questioner_first_hint_returns_2_out_of_3_chars_in_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        actual = s.first_hint()
        self.assertEqual(actual, "O__ __n__C__w__!__h__'__ __l__e__!")

    def test_questioner_second_hint_returns_no_vowels_in_answer(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        s = Subject(Connection(), question, Questions_Asked(), Player_Scores(), Timer())
        actual = s.second_hint()
        self.assertEqual(actual, "_MG H_n! Ch_w__! Th_y'r_ _ll h_r_!")

    def test_questioner_asks_a_question_to_the_chat_to_start(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        mock_connection = Connection()
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())
        s.start()
        self.assertEqual(mock_connection._message, "What's a Diorama?")

    def test_questioner_lets_the_chat_know_its_moving_on(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        mock_connection = Connection()
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())
        s.go()
        self.assertTrue(mock_connection._message in Chat.unanswered_questions)

    def test_questioner_logs_that_it_is_done_with_its_question(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        mock_questions_asked = Questions_Asked()
        s = Subject(Connection(), question, mock_questions_asked, Player_Scores(), Timer())
        s.end()
        self.assertEqual(mock_questions_asked._log[0], question)

    def test_questioner_ignores_incorect_answers_from_connection(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        mock_connection = Connection()
        mock_connection.last_response = ("trivvy_fan", "The Wrong Answer")
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())
        s.go()
        self.assertTrue(mock_connection._message in Chat.unanswered_questions)

    def test_questioner_has_a_strict_oder_to_its_message_flow(self):
        question = {
            'Ask': "What also floats in water?",
            'Answer': "A Duck!"
        }
        mock_connection = Connection()
        mock_timer = Timer()
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())
        s.go()
        self.assertEqual(len(mock_connection._message_list), 4)
        self.assertEqual(s.ask, mock_connection._message_list[0])
        self.assertEqual(s.first_hint(), mock_connection._message_list[1])
        self.assertEqual(s.second_hint(), mock_connection._message_list[2])
        self.assertTrue(mock_connection._message_list[3] in Chat.unanswered_questions)

    def test_questioner_includes_the_winners_name_when_they_answer_correctly_immediately(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        mock_connection = Connection()
        mock_connection.last_response = ("happy_lass", "OMG Han! Chewie! They're all here!")
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())
        s.go()
        self.assertTrue(mock_connection.last_response[0] in mock_connection._message)

    def test_questioner_records_the_winner_when_they_answer_correctly(self):
        question = {
            'Ask': "What's a Diorama?",
            'Answer': "OMG Han! Chewie! They're all here!"
        }
        mock_connection = Connection()
        mock_player_scores = Player_Scores()
        mock_connection.last_response = ("happy_lass", "OMG Han! Chewie! They're all here!")
        s = Subject(mock_connection, question, Questions_Asked(), mock_player_scores, Timer())
        s.go()
        self.assertEqual(mock_connection.last_response[0], mock_player_scores._score)

    def chat(self, connection, response):
        connection.last_response = response
        time.sleep(connection.seconds_per_message)

    def failure(self, connection):
        self.chat(connection, ("VILLAGER_1", "Bread!"))
        self.chat(connection, ("VILLAGER_2", "Apples!"))
        self.chat(connection, ("VILLAGER_3", "Very small rocks!"))
        self.chat(connection, ("VILLAGER_1", "Cider!"))
        self.chat(connection, ("VILLAGER_2", "Uhhh, gravy!"))
        self.chat(connection, ("VILLAGER_1", "Cherries!"))
        self.chat(connection, ("VILLAGER_2", "Mud!"))
        self.chat(connection, ("VILLAGER_3", "Churches -- churches!"))
        self.chat(connection, ("VILLAGER_2", "Lead -- lead!"))

    def success(self, connection):
        self.failure(connection)
        self.chat(connection, ("Arthur", "A duck."))
        self.chat(connection, ("knight_who_says_ni", "Ni!"))

    def test_questioner_times_out_when_no_one_answers_correctly(self):
        question = {
            'Ask': "What also floats in water?",
            'Answer': "A Duck!"
        }
        mock_connection = Connection()
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.go)
            e.submit(self.failure, mock_connection)

        self.assertTrue(mock_connection._message in Chat.unanswered_questions)

    def test_questioner_includes_the_winners_name_when_they_answer_correctly_amongst_a_stream_of_chatter(self):
        question = {
            'Ask': "What also floats in water?",
            'Answer': "A Duck!"
        }
        mock_connection = Connection()
        s = Subject(mock_connection, question, Questions_Asked(), Player_Scores(), Timer())

        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(s.go)
            e.submit(self.success, mock_connection)

        self.assertTrue("Arthur" in mock_connection._message)
