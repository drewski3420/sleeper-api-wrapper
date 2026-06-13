import logging

from .base_api import BaseApi

logger = logging.getLogger(__name__)

class Player(BaseApi):
  """Retrieves player data from Sleeper."""

  def __init__(
      self,
      player_id: str,
      player_data: dict | None = None,
      all_players_data: dict | None = None,
  ):
      self.player_id = player_id
      self.__dict__.update(metadata)
      self._all_players_data = all_players_data
      self._player_data = player_data or self._get_metadata()

      self.first_name = self._player_data.get('first_name')
      self.last_name = self._player_data.get('last_name')
      self.full_name = self._get_full_name()
      self.position = self._player_data.get('position')
      self.stats = self._player_data.get('stats')

  def _get_metadata(self) -> Dict:
    if self._all_players_data:
      return self._all_players_data[self.player_id]

  def _get_full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"
