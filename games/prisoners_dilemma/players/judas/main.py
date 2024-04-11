class PlayerController:
    """
    Judas: A player who cooperates until they are winning and defects when they start losing.
    """

    def __init__(self, payoff_matrix: dict, game_state: list, valid_moves: list):
        self.valid_moves = valid_moves
        self.payoff_matrix = payoff_matrix
        self.game_state = game_state

    def pick_move(self):
        print("Judas Move")
