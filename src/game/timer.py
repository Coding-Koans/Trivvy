class Timer:

    # Needs to know about the connection's seconds_per_message
    #    so that it can guage it's timing against that rythm

    # Needs to know about the configuration
    #    so that it can calibrate itself based on the admin's config

    # Should it be called from Go? Game? Round? Who has access to config?

    # example things it cares about:
    #  Should it care about the hinttime values,
    #  or should that be coordinated with a single time value?
    #   trivia_hinttime_1 = 30
    #   trivia_hinttime_2 = 60
    #   trivia_skiptime = 90
    #   trivia_questiondelay = 8

    # Irrelevant Config values:
    #?  trivia_filename = triviaset <= rename?
    #   trivia_bonusvalue = 3
    #   trivia_filetype = csv
    #   trivia_questions = 4

    def start_question_timer(self):
        self._times_asked = 0

    def question_time_up(self):
        self._times_asked += 1
        return self._times_asked >= 18

    def question_hint_1_up(self):
        return self._times_asked >= 4

    def question_hint_2_up(self):
        return self._times_asked >= 8