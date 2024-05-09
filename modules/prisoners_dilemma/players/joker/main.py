import random


class PlayerController:
    """
    Joker: A player who randomly cooperates or defects. Because "Chaos is Fair".
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "joker"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        choice = random.choice([-1, 1])
        if choice > 0:
            return "cooperate"
        else:
            return "defect"
