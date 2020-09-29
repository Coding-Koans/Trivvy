import time

class Timer:

    def __init__(self, connection_poll_tempo, config_settings):
        self.settings = config_settings
        self.tempo = connection_poll_tempo
        self._times_asked = 0

    def start_question_timer(self):
        self._times_asked = 0

    def question_time_up(self):
        self._times_asked += 1
        return self._times_asked >= self.q_max_asks()

    def question_hint_1_up(self):
        return self._times_asked >= self.h1_max_asks()

    def question_hint_2_up(self):
        return self._times_asked >= self.h2_max_asks()

    def wait(self):
        time.sleep(self.settings['wait'])

    def q_max_asks(self):
        return self.max_for('times_up')

    def h1_max_asks(self):
        return self.max_for('hint_1_up')

    def h2_max_asks(self):
        return self.max_for('hint_2_up')

    def max_for(self, setting):
        return self.settings[setting] / self.tempo