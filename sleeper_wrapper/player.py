import logging

from .base_api import BaseApi

logger = logging.getLogger(__name__)

class Player(BaseApi):
  def __init__(
      self,
      player_id: str,
      player_data: dict | None = None,
  ):
      self.player_id = player_id
      self._player_data = player_data

      self.first_name = self._player_data.get('first_name')
      self.last_name = self._player_data.get('last_name')
      self.full_name = self._get_full_name()
      self.position = self._player_data.get('position')
      self.stats = self._player_data.get('stats')

  def __str__(self):
    return f"{self.position} {self.full_name}"

  def _get_full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"
