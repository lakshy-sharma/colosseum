import random


def roundrobin(players: list, shuffle: bool = True) -> dict:
    """
    This functions build the fixtures using the roundrobin method.
    The supported methods are doubleroundrobin and singleroundrobin.

    Args:
        players (list): The players list for generating the matchups.
        shuffle (bool): This variable defines whether the shuffling is enabled or not. (default is True)

    Returns:
        dict: A dictionary containing the fixtures.
    """
    matchups = []
    registered_players = []
    for player in players:
        if player in registered_players:
            continue
        else:
            registered_players.append(player)
            eligible_opponents = [
                x for x in players if x != player and x not in registered_players
            ]
            for opponent in eligible_opponents:
                matchups.append([player, opponent])

    if shuffle:
        random.shuffle(matchups)

    fixtures = {}
    fixture_id = 0
    for matchup in matchups:
        fixtures[fixture_id] = matchup
        fixture_id += 1
    return fixtures
