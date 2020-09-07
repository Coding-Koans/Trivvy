import unittest
import os
from src.game.records.questions_asked import Questions_Asked as Subject

class Questions_Asked_TestCase(unittest.TestCase):
    def cleanup(self, filename):
        if os.path.exists(f"{filename}.txt"):
            os.remove(f"{filename}.txt")

    def skip_test_questions_asked_log_creates_a_log_with_a_single_entry_upon_creation(self):
        pass

    def skip_test_questions_asked_log_updates_the_log_with_a_new_entry(self):
        pass

    def skip_test_questions_asked_clear_game_replaces_the_log_with_an_empty_list(self):
        pass

    def skip_test_questions_asked_log_returns_the_current_logged_questions(self):
        pass