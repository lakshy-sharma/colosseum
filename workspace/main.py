import sys
import yaml
from games import PrisonersDilemmaGameController


class ColosseumController:

    def __init__(self, game_type: str, configurations: dict) -> None:
        self.game_type = game_type
        self.configurations = configurations

    def process_results(self, results: dict) -> None:
        """
        This function collects the results and creates animations highlighting their strategies and payoffs.
        """
        print(f"Scoreboard: {results}")

    def start(self) -> None:
        """
        This function starts the game and passes the results to a function which can buffer the results as required.
        """
        if self.game_type == "prisoners_dilemma":
            # Start the game with the players.
            game_controller = PrisonersDilemmaGameController(
                configurations=self.configurations
            )
            game_results = game_controller.start()

            # Process the output and save the findings.
            self.process_results(game_results)

        else:
            print("Game not supported.")

        return None


def read_configurations(config_path: str) -> dict:
    """
    This function reads the configurations and validates them.

    Args:
        config_file (str): The main configurations file.

    Returns:
        dict: Returns a dictionary containing the confiugrations.
    """
    with open(config_path, "r") as config_file:
        configurations = yaml.load(config_file, Loader=yaml.SafeLoader)

    return configurations


def main() -> None:
    """
    Entrypoint for the complete program.
    """
    game_type = sys.argv[1]
    configurations = read_configurations(config_path="config.yaml")
    game_controller = ColosseumController(
        game_type=game_type, configurations=configurations
    )
    game_controller.start()


if __name__ == "__main__":
    main()
