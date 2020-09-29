from src.messages import Chat
from src.game.round import Round

class Game:

    def __init__(self, connection, questions, questions_asked, player_scores, timer):
        self.connection = connection
        self.questions = questions
        self.questions_asked = questions_asked
        self.player_scores = player_scores
        self.timer = timer
        self.rounds = []

    def init_rounds(self):
        game_qs = self.list_by_rounds(self.questions)
        return [self.init_r(round_questions) for round_questions in game_qs]

    def init_r(self, round_questions):
        return Round(self.connection, round_questions, self.questions_asked, self.player_scores, self.timer)

    def list_by_rounds(self, questions):
        game_qs = []
        for q in questions:
            if q not in self.questions_asked.all_logged():
                self.add(q, game_qs) if game_qs else game_qs.append([q])
        return game_qs

    def add(self, question, game_questions):
        question_is_the_first_in_a_new_round = True
        for round_questions in game_questions:
            if question['Round'] == round_questions[0]['Round']:
                round_questions.append(question)
                question_is_the_first_in_a_new_round = False
        if question_is_the_first_in_a_new_round:
            game_questions.append([question])

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.rounds = self.init_rounds()
        self.connection.send(Chat.new_game(self.player_scores.top_players()))

    def run(self):
        self.rounds[0].go()

    def end(self):
        if len(self.rounds) == 1:
            self.questions_asked.clear_all()
            self.connection.send(Chat.end_game(self.player_scores.game_winners()))
            self.player_scores.score_winners()
            self.player_scores.reset_scores_for_next_game()
