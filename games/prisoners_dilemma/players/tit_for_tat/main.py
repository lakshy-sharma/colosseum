class PlayerController:
    """
    Tit for Tat: A player who cooperates until the other prisoner defects.
                Once defection occurs it retaliates immediately.
    """

    def __init__(
        self,
        payoff_matrix: dict,
        game_state: list,
        valid_moves: list,
        scoreboard: dict,
    ):
        self.player_name = "tit_for_tat"
        self.valid_moves = valid_moves
        self.payoff_matrix = payoff_matrix
        self.game_state = game_state
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        if len(self.game_state) == 0:
            return "cooperate"
        for player in self.game_state[-1]:
            if player == self.player_name:
                pass
            else:
                if self.game_state[-1][player] == "cooperate":
                    return "cooperate"
                else:
                    return "defect"

        return "cooperate"
