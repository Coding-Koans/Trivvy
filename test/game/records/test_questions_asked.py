import unittest
from test.test_helpers.file_system import cleanup
from src.game.records.questions_asked import Questions_Asked as Subject

class Questions_Asked_TestCase(unittest.TestCase):
    file_name = "mock_questions_asked"
    question = {
        'Ask': "What's a Diorama?",
        'Answer': "OMG Han! Chewie! They're all here!"
    }

    def test_questions_asked_log_creates_a_log_with_a_single_entry_upon_creation(self):
        given = Subject(self.file_name)
        actual = given.all_logged()
        cleanup(self.file_name)
        self.assertEqual(actual, [])

    def test_questions_asked_log_updates_the_log_with_a_new_entry(self):
        given = Subject(self.file_name)

        given.log(self.question)

        actual = given.all_logged()
        cleanup(self.file_name)
        self.assertEqual(actual, [ self.question ])

    def test_questions_asked_log_updates_the_log_with_a_ditional_entries(self):
        given = Subject(self.file_name)

        given.log(self.question)
        given.log(self.question)
        given.log(self.question)

        actual = given.all_logged()
        cleanup(self.file_name)
        self.assertEqual(actual, [ self.question, self.question, self.question ])

    def test_questions_asked_clear_game_replaces_the_log_with_an_empty_list(self):
        given = Subject(self.file_name)
        given.log(self.question)
        given.log(self.question)
        given.log(self.question)

        given.clear_all()

        actual = given.all_logged()
        cleanup(self.file_name)
        self.assertEqual(actual, [])
