from typing import Union

from .base_api import BaseApi
from .player import Player
from .user import User

class Pick:
  """The data associated with a pick in a Sleep draft.

  Attributes:
    overall_pick: int
      Overall pick number
    round_number: int
      Pick's round number
    round_pick_number: int
      Pick Number within round
    roster_id: int
      Roster ID of picking team
    team_name: str
      Team Name of picking team
    user_id: int
      User ID of picking team
    player_id: int
      Sleeper ID of player
#    metadata: Player
#      Raw metadata of Player object
  """
  def __init__(self, data: dict, league_users: dict[int, User]):
    self._data = data
    self.pick_no = self._data.get('pick_no')
    self.player_data = self._data.get('metadata')
    self.player_id = self.player_data.get('player_id')
    self.picked_by = self._data.get('picked_by')
    self._league_users = league_users
#    self.__dict__.update(data) #expand all properties
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
