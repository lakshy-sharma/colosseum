class PlayerController:
    """
    Judas: An envious player who cooperates only if they are winning and starts defecting when they start losing.
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "judas"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        if self.scoreboard[self.name] >= self.scoreboard[self.opponent]:
            return "cooperate"
        else:
            return "defect"
