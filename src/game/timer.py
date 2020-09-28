class Timer:

    # Needs to know about the connection's seconds_per_message
    #    so that it can guage it's timing against that rythm

    # Needs to know about the configuration
    #    so that it can calibrate itself based on the admin's config

    # it be called from Go, knows about hat it cares about

    # example things it cares about:
        # {
        #     self.trivia_hinttime_1,
        #     self.trivia_hinttime_2,
        #     self.trivia_skiptime,
        #     self.trivia_questiondelay,
        # }

    def __init__(self, connection_poll_tempo, config_settings):
        self.settings = config_settings
        self.tempo = connection_poll_tempo

    def start_question_timer(self):
        self._times_asked = 0

    def question_time_up(self):
        self._times_asked += 1
        return self._times_asked >= 18

    def question_hint_1_up(self):
        return self._times_asked >= 4

    def question_hint_2_up(self):
        return self._times_asked >= 8