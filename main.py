# License: GNU GPLv3
# Author: Lakshy Sharma
# Description: This is the main controller file for the colosseum engine. It will be used for running all my AI models and mathematical research projects.
# Language: Python

import sys
import yaml
import os
import importlib

def read_configurations(config_path: str) -> dict:
    """
    This function reads the configurations and validates them.

    Args:
        config_file (str): The main configurations file.

    Returns:
        dict: Returns a dictionary containing the configurations.
    """
    with open(config_path, "r") as config_file:
        configurations = yaml.load(config_file, Loader=yaml.SafeLoader)

    return configurations


def main() -> None:
    """
    This function loads the research modules and starts them as requested by the user.
    We make use of importlib module to create a plugin architecture.

    Args:
        None
    
    Returns:
        None
    """
    research_module_name = sys.argv[1]
    loaded_configs = read_configurations(config_path="config.yaml")
    loaded_modules = os.listdir("./modules")

    # Initialize the required research module.
    if research_module_name in loaded_modules:
        research_module = importlib.import_module(f".modules.{research_module_name}", package=".")
    else:
        print("Research Module not Found. Please place your code in modules folder.")

    research_module.ResearchController(configurations=loaded_configs)
    research_module.start()


if __name__ == "__main__":
    main()
