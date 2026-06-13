
from typing import Union

from .base_api import BaseApi
from .all_players import AllPlayers
from .user import User
#from .player import Player

class Team:
  def __init__(self, data: dict):
#    all_players = Players()
    self._data = data
    self.roster = None
    self.team_name = self._data['user']['metadata'].get('team_name') or self._data['user']['display_name']
    self.user = self._data.get('user')

  def __str__(self):
    return f"Team {self.team_name} owned by {self.user['display_name']}"
#    self.owner = data.get('user')
#    self.players = self._get_players()

#  def _get_players(self) -> List[Player]:
#    return [Player(player) for player in self.players]
#
#  def _get_player(self, player_info: dict) -> Player:
#    return Player(player_info)

#  def _get_round_pick_number(self, overall_pick: int) -> int:
#    return ((overall_pick - 1) % 8) + 1

#  def get_roster(self) -> List[Player]:
#    return [
#      self.players.get_player(pid)
#      for pid in (data.get('players') or [])
#    ]

