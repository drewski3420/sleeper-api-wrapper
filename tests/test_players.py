from sleeper_wrapper import Player

def test_get_trending_players() -> None:
	players = Player()
	added = players.get_trending_players("nfl","add", 1, 4)

	dropped = players.get_trending_players("nfl","drop")
