import importlib
from multiprocessing import process
import matplotlib.pyplot as plt
import matplotlib.animation as aniplt
import random
from .utils.fixtures_generators import roundrobin
import multiprocessing


class PrisonersDilemmaGameController:
    """
    This game controller is used for controlling the game.
    Currently the implementation is single threaded but the plan is to convert it into a multithreaded where each round is run inside its own thread.
    """

    def __init__(self, configurations) -> None:
        self.game_type = "prisoners_dilemma"
        self.configurations = configurations

        # This list records all the moves made the players upto this point.
        # It will be passed alongwith payoff matrix on each turn to players.
        self.game_history = []
        self.global_history = []
        self.payoff_matrix = self.configurations[self.game_type]["payoff_matrix"]

        # Register players on the scoreboard.
        self.scoreboard = {}
        self.reset_scoreboard()

    def flush_game_history(self) -> None:
        """
        This function transfers clears the game history.

        Returns:
            None
        """
        self.game_history = []

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

    def score_moves(self, moves_data: dict) -> None:
        """
        This function maps the results into the scoreboard.

        Args:
            moves_data (dict): This is a dictionary based mapping of player moves.
        Returns:
            None (We update the scores into the scoreboard of class object itself)
        """
        # Register each player's move in the list
        moves = []
        players = []
        for player in moves_data:
            players.append(player)
            moves.append(moves_data[player])
        # Award points
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

    def export_graph(self, animation_data: aniplt.ArtistAnimation, round: int) -> None:
        """
        This function saves the data into a file by using the ffmpeg library.
        It has been seperated from complete program so that we can call it using the process library and make the operation fast.

        Args:
            animation_data (ArtistAnimation): A matplotlib based artist animation.
            round (int): An integer value depicting the current round for which we are saving the data.

        Returns:
            None (The operation writes data into a file.)
        """
        animation_data.save(
            f"./visuals/{self.game_type}/round{round}.mp4",
            writer=aniplt.FFMpegWriter(fps=25),
        )

    def start(self) -> None:
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

        process_store = {}
        for round in range(
            self.configurations[self.game_type]["fixture_settings"]["rounds"]
        ):
            # Create a new visualization for this round and start the animation.
            fig, ax = plt.subplots()
            fig.set_figheight(10)
            fig.set_figwidth(15)
            ax.set_title("Prisoners Dilemma Tournament")
            ax.set_xlabel("Points")
            ax.set_ylabel("Players")
            artists = []

            # Start the fixtures for this round.
            for fixture in fixtures:
                print(
                    f"Round Id: {round}, Fixture Id: {fixture}, Players: {fixtures[fixture]}, Iterations: {game_iterations}"
                )

                # Setup the players for this fixture.
                player1_controller = player_modules[
                    fixtures[fixture][0]
                ].PlayerController(
                    opponent_name=fixtures[fixture][1],
                    payoff_matrix=self.payoff_matrix,
                    game_history=self.game_history,
                    global_history=self.global_history,
                    scoreboard=self.scoreboard,
                )
                player2_controller = player_modules[
                    fixtures[fixture][1]
                ].PlayerController(
                    opponent_name=fixtures[fixture][0],
                    payoff_matrix=self.payoff_matrix,
                    game_history=self.game_history,
                    global_history=self.global_history,
                    scoreboard=self.scoreboard,
                )

                # Perform the game iterations for this fixture.
                for i in range(game_iterations):
                    player1_move = player1_controller.make_move()
                    player2_move = player2_controller.make_move()

                    # Award points based on moves.
                    self.score_moves(
                        moves_data={
                            player1_controller.name: player1_move,
                            player2_controller.name: player2_move,
                        }
                    )

                    # Append the moves into history.
                    self.game_history.append(
                        {
                            player1_controller.name: player1_move,
                            player2_controller.name: player2_move,
                        }
                    )
                    # self.global_history.append(
                    #     {
                    #         "round": round,
                    #         "fixture": fixture,
                    #         "moves": [{
                    #             player1_controller.name: player1_move,
                    #             player2_controller.name: player2_move,
                    #         }],
                    #     }
                    # )
                    # Plot the scores on the map.
                    colors = ["tab:blue", "tab:red", "tab:green", "tab:purple"]
                    container = ax.barh(
                        list(self.scoreboard.keys()),
                        list(self.scoreboard.values()),
                        color=colors,
                    )
                    artists.append(container)

                # Delete the player objects.
                del player1_controller
                del player2_controller
                # Delete the game history.
                self.flush_game_history()

            # Save the plot for this round in a file.
            # This must start as a new process and final program should wait until it quits.
            ani = aniplt.ArtistAnimation(fig=fig, artists=artists, interval=1)
            process_store[round] = multiprocessing.Process(
                target=self.export_graph, args=(ani, round)
            )
            process_store[round].start()

            # Reset the scoreboard for next round.
            self.reset_scoreboard()

        print("Waiting for file writer processes to join back.")
        for round in process_store:
            process_store[round].join()

        return None
