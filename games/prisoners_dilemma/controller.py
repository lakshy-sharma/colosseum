import importlib
import random
import time
from .utils.fixtures_generators import roundrobin


class PrisonersDilemmaGameController:

    def __init__(self, configurations) -> None:
        self.game_type = "prisoners_dilemma"
        self.configurations = configurations

        # This list records all the moves made the players upto this point.
        # It will be passed alongwith payoff matrix on each turn to players.
        self.game_state = []
        self.payoff_matrix = self.configurations[self.game_type]["payoff_matrix"]

        # Register players on the scoreboard.
        self.scoreboard = {}
        for player in self.configurations[self.game_type]["players"]:
            self.scoreboard[player] = 0

    def register_players(self) -> dict:
        """
        This function loads the players and passes them back into the main program loop.
        """
        # Initiate the modules for each player.
        player_modules = {}
        for player in self.configurations[self.game_type]["players"]:
            player_modules[player] = importlib.import_module(
                f".players.{player}", package=f"games.{self.game_type}"
            )

        return player_modules

    def generate_fixtures(self) -> dict:
        """
        This function creates the fixtures for the matches to be played between the players.
        """
        fixtures = {}

        # Create fixtures.
        if "roundrobin" in self.configurations[self.game_type]["format"]:
            fixtures = roundrobin(
                players=self.configurations[self.game_type]["players"],
                format=self.configurations[self.game_type]["format"],
            )
        else:
            fixtures = roundrobin(
                players=self.configurations[self.game_type]["players"],
                format=self.configurations[self.game_type]["format"],
            )

        return fixtures

    def score_results(self, player_moves: dict) -> None:
        moves = []
        players = []

        # Register each player's move in the list
        for player in player_moves:
            self.game_state.append(player_moves)
            players.append(player)
            moves.append(player_moves[player])

        if (moves[0] == "cooperate") and (moves[1] == "cooperate"):
            self.scoreboard[players[0]] += 2
            self.scoreboard[players[1]] += 2
        elif (moves[0] == "cooperate") and (moves[1] == "defect"):
            self.scoreboard[players[0]] += 0
            self.scoreboard[players[1]] += 3
        elif (moves[0] == "defect") and (moves[1] == "cooperate"):
            self.scoreboard[players[0]] += 3
            self.scoreboard[players[1]] += 0
        elif (moves[0] == "defect") and (moves[1] == "defect"):
            self.scoreboard[players[0]] += 1
            self.scoreboard[players[1]] += 1

        return None

    def start(self) -> dict:
        """
        1. Start game iterations.
        2. Collect the result in a seperate dictionary and return to the main caller.
        """

        player_modules = self.register_players()
        fixtures = self.generate_fixtures()
        game_iterations = random.randrange(
            start=self.configurations[self.game_type]["min_iterations"],
            stop=self.configurations[self.game_type]["max_iterations"],
            step=1,
        )

        # Start the game.
        for fixture in fixtures:
            print(
                f"Game Fixture Id: {fixture}. Players: {fixtures[fixture]}. Iterations: {game_iterations}"
            )
            for i in range(game_iterations):
                # Pass the payoff matrix and the game state to each player.
                # Fetch their responses and award points based on their moves.
                player_moves = {}
                for player in fixtures[fixture]:
                    player_controller = player_modules[player].PlayerController(
                        valid_moves=self.configurations[self.game_type]["valid_moves"],
                        payoff_matrix=self.payoff_matrix,
                        game_state=self.game_state,
                    )
                    player_moves[player] = player_controller.make_move()

                self.score_results(player_moves)
                time.sleep(0.001)

        return self.scoreboard
