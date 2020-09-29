from src.game.records.file_system_orm import FS_ORM

class Player_Scores():
    def __init__(self, file_name):
        blank_records = {}
        self.fs = FS_ORM(file_name, blank_records)
        self.scores = self.fs.get_records()

    def score(self, player):
        self.scores = self.fs.get_records()
        if player in self.scores.keys():
            self.up_score(player)
        else:
            self.add_to_board(player)
        self.fs.save_records(self.scores)

    def up_score(self, player):
        self.scores[player]['round_points'] += 1
        self.scores[player]['game_points'] += 1

    def add_to_board(self, player):
        self.scores[player] = {
            "round_points": 1,
            "game_points": 1,
            "game_wins": 0
        }

    def score_winners(self):
        self.scores = self.fs.get_records()
        top_score = 1
        for player, scores in self.scores.items():
            if self.scores[player]["game_points"] > top_score:
                top_score = self.scores[player]["game_points"]
        for player, score in self.scores.items():
            if self.scores[player]["game_points"] == top_score:
                self.scores[player]["game_wins"] += 1
        self.fs.save_records(self.scores)

    def reset_scores_for_next_round(self):
        self.scores = self.fs.get_records()
        self.reset("round_points")
        self.fs.save_records(self.scores)

    def reset_scores_for_next_game(self):
        self.scores = self.fs.get_records()
        self.reset("round_points")
        self.reset("game_points")
        self.fs.save_records(self.scores)

    def reset(self, thing_to_be_reset):
        for score in self.scores.values():
            score[thing_to_be_reset] = 0

    def round_winners(self):
        return self.top_3_by("round_points")

    def game_winners(self):
        return self.top_3_by("game_points")

    def top_players(self):
        return self.top_3_by("game_wins")

    def top_3_by(self, point_type):
        player_tuples = []
        for player, record in self.scores.items():
            if record[point_type] > 0:
                player_tuples.append((player, record[point_type]))
        sorted_players = sorted(player_tuples, key=lambda player: player[1], reverse=True)
        return sorted_players[:3]
