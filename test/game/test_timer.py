import unittest
from src.game.timer import Timer as Subject

class TimerTestCase(unittest.TestCase):
    def test_timer_max_for_returns_the_number_of_times_questioner_should_iterate(self):
        setting_key = 'max_for_doesnt_care_about_specifics'
        times_per_second = 120
        seconds_to_wait = 2

        tempo = 1 / times_per_second
        settings = {
            setting_key: seconds_to_wait
        }
        subject = Subject(tempo, settings)

        actual = subject.max_for(setting_key)
        expected = times_per_second * seconds_to_wait
        self.assertEqual(actual, expected)

    def test_timer_max_for_returns_a_different_number_of_times_questioner_should_iterate(self):
        setting_key = 'max_for_doesnt_care_about_specifics'
        times_per_second = 1000
        seconds_to_wait = 8

        tempo = 1 / times_per_second
        settings = {
            setting_key: seconds_to_wait
        }
        subject = Subject(tempo, settings)

        actual = subject.max_for(setting_key)
        expected = times_per_second * seconds_to_wait
        self.assertEqual(actual, expected)