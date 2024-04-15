import random


class PlayerController:
    """
    Better and Better: This player cooperates with a probability of current_round / 1000. this means it gets better as the game proceeds.
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "better_and_better"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        current_round = len(self.game_history) + 1
        cooperation_probability = 1 - (current_round / 1000)
        if random.random() <= cooperation_probability:
            return "cooperate"
        else:
            return "defect"
