from src.game.records.triviaset import Trivia_Set
from src.game.records.configuration import Trivia_Game_Configuration
from src.game.timer import Timer
from src.game.game import Game
from src.messages import Log as report

class Go:
    command = "!go"
    validate = [ "admin_only" ]

    def __init__(self, timer_settings_txt, question_csv, questions_asked, player_scores, log = print):
        self.timer_settings_txt = timer_settings_txt
        self.csv_filename = question_csv
        self.questions_asked = questions_asked
        self.player_scores = player_scores
        self.log = log
        self.game_running = False

    def tuple(self):
        return (Go.command, self.run_the_next_trivia_round, Go.validate)

    def run_the_next_trivia_round(self, connection, message):
        if self.game_running:
            self.log(report.in_progress(message[0], message[1]))
        else:
            self.lock_run_round(connection)

    def lock_run_round(self, connection):
        self.game_running = True
        self.init_and_run_round(connection)
        self.game_running = False

    def init_and_run_round(self, connection):
        csv = self.get_questions()
        timer = self.get_timer(connection.seconds_per_message)
        if not csv.error:
            self.run_round(connection, csv, timer)

    def get_questions(self):
        return Trivia_Set(self.csv_filename, self.log)

    def get_timer(self, tempo):
        config = Trivia_Game_Configuration(self.timer_settings_txt, self.log)
        settings = config.get_trivia_constants()
        return Timer(tempo, settings)

    def run_round(self, connection, csv, timer):
        questions = csv.get_questions()
        game = Game(connection, questions, self.questions_asked, self.player_scores, timer)
        game.go()
