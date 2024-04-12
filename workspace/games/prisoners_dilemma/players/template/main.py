import nashpy


class PlayerController:
    """
    Template: A player designed to act as a template for new comers.

    Useful Tips:
    1. You can use the payoff matrix to calculate the nash equilibrium and play accordingly. The nashpy library has been installed for your needs.
    2. You can use the game history to see how your opponent has responded to your moves and make decisions.
    3. You can access the global history to see how other players are playing and make decisions accordingly.
    4. The scoreboard provides latest game scores for you, the opponent and others in the game.

    Important Note:
        The self.name attribute must match the player name you have given in config.yaml else you wont be able to recognise yourself during the game.
    """

    def __init__(
        self,
        opponent_name: str,
        payoff_matrix: dict,
        game_history: list,
        global_history: list,
        scoreboard: dict,
    ):
        self.name = "template"
        self.opponent = opponent_name
        self.payoff_matrix = payoff_matrix
        self.game_history = game_history
        self.global_history = global_history
        self.scoreboard = scoreboard

    def make_move(self) -> str:
        return "cooperate"
