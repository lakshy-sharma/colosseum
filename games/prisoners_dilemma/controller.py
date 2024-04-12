import importlib
import matplotlib.pyplot as plt
import matplotlib.animation as aniplt
import random
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
        self.reset_scoreboard()

    def reset_scoreboard(self) -> None:
        """
        This function resets the scoreboard.

        Returns:
            None
        """
        for player in self.configurations[self.game_type]["players"]:
            self.scoreboard[player] = 0

    def register_player_modules(self) -> dict:
        """
        This function loads the players and passes them back into the main program loop.

        Returns:
            dict: A dictionary containing the player modules mapped to their names.
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

        Returns:
            dict: A dictionary which contains all the fixtures for a game.
        """
        fixtures = {}

        # Create fixtures.
        if (
            "roundrobin"
            in self.configurations[self.game_type]["fixture_settings"]["format"]
        ):
            fixtures = roundrobin(
                players=self.configurations[self.game_type]["players"]
            )
        else:
            fixtures = roundrobin(
                players=self.configurations[self.game_type]["players"]
            )

        return fixtures

    def score_results(self, player_moves: dict) -> None:
        """
        This function maps the results into the scoreboard.

        Args:
            player_moves (dict): This is a dictionary based mapping of player moves.
        Returns:
            None
        """
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

        Returns:
            dict: A dictionary containing the final scoreboard of the game.
        """

        player_modules = self.register_player_modules()
        fixtures = self.generate_fixtures()
        game_iterations = random.randrange(
            start=self.configurations[self.game_type]["fixture_settings"][
                "min_iterations"
            ],
            stop=self.configurations[self.game_type]["fixture_settings"][
                "max_iterations"
            ],
            step=1,
        )

        for round in range(
            self.configurations[self.game_type]["fixture_settings"]["rounds"]
        ):
            # Create a new visualization for this round and start the animation.
            fig, ax = plt.subplots()
            artists = []

            # Start the fixture games for this round.
            for fixture in fixtures:
                print(
                    f"Round Id: {round}, Fixture Id: {fixture}, Players: {fixtures[fixture]}, Iterations: {game_iterations}"
                )
                # Perform the itertaions for this fixture.
                for i in range(game_iterations):
                    player_moves = {}
                    for player in fixtures[fixture]:
                        player_controller = player_modules[player].PlayerController(
                            valid_moves=self.configurations[self.game_type][
                                "valid_moves"
                            ],
                            payoff_matrix=self.payoff_matrix,
                            game_state=self.game_state,
                            scoreboard=self.scoreboard,
                        )
                        player_moves[player] = player_controller.make_move()
                    self.score_results(player_moves)

                    # Plot the scores on the map.
                    colors = ["tab:blue", "tab:red", "tab:green", "tab:purple"]
                    container = ax.barh(
                        list(self.scoreboard.keys()),
                        list(self.scoreboard.values()),
                        color=colors,
                    )
                    artists.append(container)

            # Finalize the plot and save it.
            ani = aniplt.ArtistAnimation(fig=fig, artists=artists, interval=10)
            ani.save(
                f"./visuals/{self.game_type}/round{round}.gif",
                writer="pillow",
            )
            # After each round reset the scoreboard.
            self.reset_scoreboard()

        return self.scoreboard
