from src.game.records.questions_asked import Questions_Asked
from src.game.records.players import Players

from .go import Go
from .stop import stop

class all:
    def commands():
        return [
            Go('triviaset.csv', Questions_Asked(), Players("player_scores")).tuple(),
            stop.tuple(),
        ]
