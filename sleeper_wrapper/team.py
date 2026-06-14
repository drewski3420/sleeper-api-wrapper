from typing import Union

from .base_api import BaseApi
from .all_players import AllPlayers
from .user import User

class Team:
  def __init__(self, data: dict):
    self._data = data
    self.roster_id = self._data.get('roster_id')
    self.team_name = self._data['user']['metadata'].get('team_name') or self._data['user']['display_name']
    self.user = self._data.get('user')

  def __str__(self):
    return f"Team {self.team_name} owned by {self.user['display_name']}"

