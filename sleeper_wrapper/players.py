import os
import logging
import json

from .base_api import BaseApi
from .player import Player

logger = logging.getLogger(__name__)

class Players(BaseApi):
  """Retrieves player data from Sleeper."""
  _cache = None

  def __init__(self, sport: str = "nfl"):
    self._sport = sport
    self._players_fn = "players.json"
    self.players = self._get_players()

    if Players._cache is None:
      Players._cache = self._get_players()

    self.players = Players._cache

  def _get_players(self) -> Dict:
    if not os.path.exists(self._players_fn):
      self._populate_players_file()
    with open(self._players_fn,'r') as f:
      return json.loads(f.read())

  def _populate_players_file(self) -> dict:
    with open(self._players_fn, 'w') as f:
      data = self._call(f"https://api.sleeper.app/v1/players/{self._sport}")
      f.write(json.dumps(data))

  def get_player(self, player_id: str | int) -> Player:
    player_id = str(player_id)

    metadata = self.players.get(player_id)

    if metadata is None:
      logger.warning(f"Player {player_id} not found")
      return Player(player_id)

    return Player(player_id, metadata)
#
#  def get_trending_players(self, sport: str, add_drop: str = "add", hours: int = 24, limit: int = 25) -> list:
#    """Gets trending players from Sleeper.
#
#    Retrieves the player ID and number of adds / drops for that player
#    during the specified lookback hours.
#
#    Args:
#      sport: str
#      The sport to retrieve the players. Options include "nfl",
#      "nba", and "lcs".
#      add_drop: str
#        Type of action to retreive. Either "add" or "drop".
#      hours: int
#        The number of hours to look back.
#      limit: int
#        The number of players to retrieve.
#
#    Returns:
#      A list of dicts containing the player ID and a count of the adds /
#      drops.
#    """
#
#
#    message = """If you use this trending data, please attribute Sleeper.
#
#    Copy the code below to embed it in your app:
#    <iframe src="https://sleeper.app/embed/players/nfl/trending/add?lookback_hours=24&limit=25" width="350" height="500" allowtransparency="true" frameborder="0"></iframe>
#    """
#    logger.info(message)
#    return self._call("https://api.sleeper.app/v1/players/{}/trending/{}?lookback_hours={}&limit={}".format(sport, add_drop, hours, limit))
