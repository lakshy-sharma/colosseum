import importlib
import matplotlib.pyplot as plt
import matplotlib.animation as aniplt
import random
import json
import multiprocessing
from .utils.fixtures_generators import roundrobin


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

    def score_moves(self, player1_move: str, player2_move: str) -> tuple[int, int]:
        """
        This function maps the results into the scoreboard.

        Args:
            player1_move (str): The move made by the first player.
            player2_move (str): The move made by the second player.

        Returns:
            tuple[int,int]: A tuple of strings containing the points to be awarded to each player.
        """
        if (player1_move == "cooperate") and (player2_move == "cooperate"):
            return (2, 2)
        elif (player1_move == "cooperate") and (player2_move == "defect"):
            return (0, 3)
        elif (player1_move == "defect") and (player2_move == "cooperate"):
            return (3, 0)
        elif (player1_move == "defect") and (player2_move == "defect"):
            return (1, 1)
        else:
            print(
                f"Invalid move by the players: Player1: {player1_move}, Player2: {player2_move}. Please fix this."
            )
            exit(0)

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

    def analyse_global_history(self) -> None:
        """
        This function analyzes the global history and generates pre-programmed graphical insights.
        The function is isolated to ensure maximal parallelization and isolation from rest of program.

        Args:
            None
        Returns:
            None
        """

        # Plotting the progress of each player in a bar chart animation.
        total_rounds = self.configurations[self.game_type]["fixture_settings"]["rounds"]
        process_store = {}
        for round in range(total_rounds):
            figure, ax = plt.subplots()
            figure.set_figheight(10)
            figure.set_figwidth(15)
            ax.set_title(f"Round: {round}")
            ax.set_xlabel("Points")
            ax.set_ylabel("Players")
            artists = []

            # Filter all fixtures for this round. from global history.

            round_fixtures_list = [
                d for d in self.global_history if d["round"] == round
            ]
            for fixtures_data in round_fixtures_list:
                for move in fixtures_data["moves_data"]:
                    players = list(move.keys())
                    player_moves = list(move.values())

                    # Get the scores for the above players.
                    player1_score, player2_score = self.score_moves(
                        player1_move=player_moves[0], player2_move=player_moves[0]
                    )

                    # We need to score each move in the moves data.
                    container = ax.barh(
                        list(self.scoreboard.keys()),
                        list(self.scoreboard.values()),
                    )
                    artists.append(container)

            ani = aniplt.ArtistAnimation(fig=figure, artists=artists, interval=1)
            process_store[round] = multiprocessing.Process(
                target=self.export_graph, args=(ani, round)
            )
            process_store[round].start()

        print("Waiting for analysis plotters to join back.")
        for round in process_store:
            process_store[round].join()
        return None

    def update_global_history(
        self, round_id: int, fixture_id: int, player1: str, player2: str
    ) -> None:
        """
        Updates the global history with game history.

        Args:
            round_id (int): The round id for this entry.
            fixture_id (int): The fixture if for this entry.
            player1 (str): The player 1 of this fixture.
            player2 (str): The player 2 of this fixture.
        Returns:
            None
        """

        self.global_history.append(
            {
                "round_id": round_id,
                "fixture_id": fixture_id,
                "player1": player1,
                "player2": player2,
                "moves_data": self.game_history,
            }
        )
        return None

    def start(self) -> None:
        """
        1. Start game iterations.
        2. Collect the result in a seperate dictionary and return to the main caller.

        Returns:
            None
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
                    player1_score, player2_score = self.score_moves(
                        player1_move, player2_move
                    )

                    # Update the scoreboard with new scores.
                    self.scoreboard[player1_controller.name] += player1_score
                    self.scoreboard[player2_controller.name] += player2_score

                    # Append the moves into history.
                    self.game_history.append(
                        {
                            player1_controller.name: player1_move,
                            player2_controller.name: player2_move,
                        }
                    )

                    # Plot the scores on the map.
                    container = ax.barh(
                        list(self.scoreboard.keys()),
                        list(self.scoreboard.values()),
                    )
                    artists.append(container)

                # Save the game history into global history.
                self.update_global_history(
                    round_id=round,
                    fixture_id=fixture,
                    player1=player1_controller.name,
                    player2=player2_controller.name,
                )

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

        # Save the history into a json file.
        print(f"Global history saved to file: ./game_data/{self.game_type}.json")
        with open(f"./game_data/{self.game_type}.json", "w") as global_history_file:
            json.dump(self.global_history, global_history_file)

        # Analyse the global history and generate relevant insights graphs.
        # print("Starting the analysis plotters.")
        # self.analyse_global_history()

        # Wait for analysis plotters to complete.
        print("Waiting for analysis plotters to join back.")
        for round in process_store:
            process_store[round].join()

        return None
