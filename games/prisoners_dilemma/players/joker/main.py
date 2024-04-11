import random


class PlayerController:

    def __init__(self, payoff_matrix: dict, game_state: list, valid_moves: list):
        self.player_name = "joker"
        self.valid_moves = valid_moves
        self.payoff_matrix = payoff_matrix
        self.game_state = game_state

    def make_move(self) -> str:
        choice = random.choice([-1, 1])
        if choice > 0:
            return "cooperate"
        else:
            return "defect"
