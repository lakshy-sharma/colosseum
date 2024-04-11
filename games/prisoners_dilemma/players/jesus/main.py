class PlayerController:
    """
    Jesus: A player who always cooperates.
    """

    def __init__(self, payoff_matrix: dict, game_state: list, valid_moves: list):
        self.valid_moves = valid_moves
        self.payoff_matrix = payoff_matrix
        self.game_state = game_state

    def make_move(self) -> str:
        return "cooperate"
