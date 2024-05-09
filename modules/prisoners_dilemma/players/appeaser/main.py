import nashpy


class PlayerController:
    """
    Appeaser: A player who tries to guess what the opponent wants and changes strategy accordingly. 
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "appeaser"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        if len(self.game_history) == 0:
            return "cooperate"

        if self.game_history[-1][self.opponent] == "defect":
            if self.game_history[-1][self.name] == "cooperate":
                return "defect"
            else:
                return "cooperate"
        else:
            return "cooperate"
