from src.game.records.questions_asked import Questions_Asked
from src.game.records.players import Players

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
            Go('triviaset.csv', Questions_Asked(self.opts["qa"]), Players(self.opts["ps"])).tuple(),
            stop.tuple(),
        ]
