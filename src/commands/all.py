from src.game.records.questions_asked import Questions_Asked
from src.game.records.player_scores import Player_Scores

from .go import Go
from .stop import stop

production_options = {
    'qa': "questions_asked",
    'ps': "player_scores"
}

class All:
    def __init__(self, options = production_options):
        self.opts = options

    def commands(self):
        return [
            Go('triviaset.csv', Questions_Asked(self.opts["qa"]), Player_Scores(self.opts["ps"])).tuple(),
            stop.tuple(),
        ]
