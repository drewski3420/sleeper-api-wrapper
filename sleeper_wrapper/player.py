import logging

from .base_api import BaseApi
#from .players import Players

logger = logging.getLogger(__name__)

class Player(BaseApi):
  """Retrieves player data from Sleeper."""

  def __init__(
      self,
      player_id: str,
      metadata: dict | None = None,
      players_data: dict | None = None,
  ):
      self.player_id = player_id
      self._players_data = players_data
      self._metadata = metadata

      self.__dict__.update(metadata)

      self.full_name = self._get_full_name()

  def metadata(self) -> Dict:
    if self._metadata is None and self._players_data:
      self._metadata = self._players_data[self.player_id]
    return self._metadata

  def _get_full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"
#  def __init__(self, player_id: int, all_players: Players):
#    self.all_players = all_players
#    self.player_id = player_id
#    self.data = self._get_player()
#    self.__dict__.update(data)
#    self.name = f"{self.first_name} {self.last_name}"
#
#
#  def _get_player() -> Dict:
#    return next((p for p in self.all_players if p.get("player_id") == self.player_id), None)
#  def get_all_players(self, sport: str = "nfl") -> dict:
#    """Gets all players from Sleeper.
#
#    Retrieves data pertaining to each player in the Sleeper, including
#    positions, biographical data, height / weight, team, and more.
#
#    Args:
#      sport: str
#      The sport to retrieve the players. Options include "nfl",
#      "nba", and "lcs".
#
#    Returns:
#      A dict of dicts where the keys are the player IDs and the values
#      contain all of the player information.
#    """
#
#    message = """Please use this call sparingly, as it is intended only to be used once per day at most to keep your player IDs updated.
#
#    Save the information to your own servers, if possible.
#    """
#    logger.info(message)
#    return self._call("https://api.sleeper.app/v1/players/nfl")
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
