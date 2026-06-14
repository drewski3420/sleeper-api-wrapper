from typing import TYPE_CHECKING

from .player import Player

if TYPE_CHECKING:
  from .team import Team
  from .user import User


class Pick:
  def __init__(
      self,
      data: dict,
      users_by_id: dict[int, "User"],
      teams_by_user_id: dict[int, "Team"],
  ):
    self._users_by_id = users_by_id
    self._teams_by_user_id = teams_by_user_id
    self._data = data
    self.pick_no = self._data.get('pick_no')
    self.player_data = self._data.get('metadata') or {}
    self.player_id = self.player_data.get('player_id')
    self.picked_by_user_id = self._data.get('picked_by')
    self.round_pick_number = self._get_round_pick_number()
    self.player = self._get_player()
    self.user = self._get_pick_user()
    self.team = self._get_pick_team()
    self.team_name = self.team.team_name if self.team else str(self.picked_by_user_id)
    self.round = self._data.get('round')

  def __str__(self):
    return f"Round: {self.round} Pick: {self.round_pick_number} (Overall {self.pick_no}) by {self.team_name}"

  def _get_player(self) -> Player:
    return Player(self.player_id, self.player_data)

  def _get_round_pick_number(self) -> int:
    team_count = len(self._teams_by_user_id)
    if team_count == 0 or self.pick_no is None:
      return 0
    return ((self.pick_no - 1) % team_count) + 1

  def _get_pick_user(self) -> "User | None":
    return self._users_by_id.get(self.picked_by_user_id)

  def _get_pick_team(self) -> "Team | None":
    return self._teams_by_user_id.get(self.picked_by_user_id)
