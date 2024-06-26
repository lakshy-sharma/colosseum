class PlayerController:
    """
    Grudger: A player who holds grudges. Strats with cooperation but defects if opponent defects anytime.
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "grudger"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard
        self.grudged = False # Start without a grudge

    def make_move(self) -> str:
        # Start with cooperation.
        if len(self.game_history) == 0:
            return "cooperate"

        if (
            self.game_history[-1][self.opponent] == "cooperate"
            and self.grudged != False
        ):
            return "cooperate"
        else:
            # Mark this player as a defector and hold a grudge.
            self.grudged = True
            return "defect"
