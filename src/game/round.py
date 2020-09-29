from src.messages import Chat
from src.game.questioner import Questioner

class Round():

    def __init__(self, connection, questions, questions_asked, player_scores, timer):
        self.connection = connection
        self.name = questions[0]['Round'] if questions else 0
        self.questions_asked = questions_asked
        self.timer = timer
        self.player_scores = player_scores
        self.questioners = self.init_questioners(questions)

    def init_questioners(self, questions):
        return [self.init_q(question) for question in questions]

    def init_q(self, question):
        return Questioner(self.connection, question, self.questions_asked, self.player_scores, self.timer)

    def go(self):
        self.start()
        self.run()
        self.end()

    def start(self):
        self.connection.send(Chat.new_round(self.name))

    def run(self):
        for questioner in self.questioners:
            questioner.go()

    def end(self):
        self.connection.send(Chat.end_round(self.player_scores.round_winners()))
        self.player_scores.reset_scores_for_next_round()
