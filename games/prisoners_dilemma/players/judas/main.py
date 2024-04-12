class PlayerController:
    """
    Judas: A player who cooperates until they are winning and defects when they start losing.
    """

    def __init__(
        self,
        payoff_matrix: dict,
        game_state: list,
        valid_moves: list,
        scoreboard: dict,
    ):
        self.player_name = "judas"
        self.valid_moves = valid_moves
        self.payoff_matrix = payoff_matrix
        self.game_state = game_state
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        my_points = self.scoreboard[self.player_name]
        for player in self.scoreboard:
            if player == self.player_name:
                pass
            else:
                opponent_points = self.scoreboard[player]
                break

        if my_points >= opponent_points:
            return "cooperate"
        else:
            return "defect"
