class PlayerController:
    """
    Tit for Tat: A player who cooperates until the other player defects. If a player defects, it retaliates immediately.
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "tit_for_tat"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard

    def make_move(self) -> str:

        # If we are at first chance then always cooperate.
        # Else perform the same move that the opponent did in previous move.
        if len(self.game_history) == 0:
            return "cooperate"
        else:
            return self.game_history[-1][self.opponent]