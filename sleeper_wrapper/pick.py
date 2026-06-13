from typing import Union

from .base_api import BaseApi
from .player import Player
from .user import User

class Pick:
  def __init__(self, data: dict, league_users: dict[int, User]):
    self._data = data
    self.pick_no = self._data.get('pick_no')
    self.player_data = self._data.get('metadata')
    self.player_id = self.player_data.get('player_id')
    self.picked_by = self._data.get('picked_by')
    self._league_users = league_users
    self.round_pick_number = self._get_round_pick_number()
    self.player = self._get_player()
    self.user = self._get_pick_user()
    self.team_name = self.user.team_name
    self.round = self._data.get('round')

  def __str__(self):
    return f"Round: {self.round} Pick: {self.round_pick_number} (Overall {self.pick_no}) by {self.team_name}"

  def _get_player(self) -> Player:
    return Player(self.player_id, self.player_data)

  def _get_round_pick_number(self) -> int:
    return ((self.pick_no - 1) % 8) + 1

  def _get_pick_user(self) -> User:
    return self._league_users.get(self.picked_by)
