def roundrobin(players: list) -> dict:
    """
    This functions build the fixtures using the roundrobin method.
    The supported methods are doubleroundrobin and singleroundrobin.
    """
    fixtures = {}
    fixture_id = 0
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
                fixtures[fixture_id] = [player, opponent]
                fixture_id += 1
    return fixtures
