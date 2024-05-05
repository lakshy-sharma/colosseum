import json

class SokobanSolver():
    """
    A sokoban solver class that takes some configuration and levels data to start solving the level with provided methods.
    The class has been provided to help parallelize the code with multiprocessing module in future.
    You can enable internal parallelization by using the enable_threading parameter.
    """
    def __init__(self, configuration: dict, level_data: dict, enable_threading: bool = False) -> None:
        self.configuration = configuration
        self.level_data = level_data
        self.game_matrix = self.level_data["game_matrix"]
        self.metadata = self.level_data["metadata"]
        return None

    def _dfs_solver(self):
        pass


    def _bfs_solver(self):
        pass


    def _astar_solver(self):
        pass

    def solve(self) -> None:
        for method in self.configuration["methods"]:
            if method == "DFS":
                self._dfs_solver()
            elif method == "BFS":
                self._bfs_solver()
            elif method == "BFS":
                self._astar_solver()
            else:
                print("Method not supported")
        return None



def load_json(path: str) -> dict:
    """
    This function can be used to read any json file.
    It returns back a simple dictionary upon successful loading or provides an empty string as an output on failure.

    Args
        path (str): The path to the json file for loading.

    Returns
        dict: The returned value is a dict with loaded json.
    """
    try:
        with open(path, "r") as levels_file:
            levels_data = json.load(levels_file)
        return levels_data
    except:
        return {}

def main() -> None:
    """
    The main entrypoint for the program.
    """

    # Load the levels and configurations data and if not possible then quit.
    configuration = load_json(path="./config.json")
    levels_data = load_json(path="./levels.json")
    
    # Create a solver for each level and start solving with the provided configuration.
    for level in levels_data.keys():
        solver = SokobanSolver(configuration=configuration, level_data=levels_data[level])
        solver.solve()

    return None

if __name__ == "__main__":
    main()