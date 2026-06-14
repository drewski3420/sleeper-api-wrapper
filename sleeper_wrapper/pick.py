from typing import TYPE_CHECKING

from .player import Player

if TYPE_CHECKING:
  from .team import Team


class Pick:
  def __init__(self, data: dict, league_teams_by_user_id: dict[int, "Team"]):
    self._league_teams_by_user_id = league_teams_by_user_id
    self._data = data
    self.pick_no = self._data.get('pick_no')
    self.player_data = self._data.get('metadata')
    self.player_id = self.player_data.get('player_id')
    self.picked_by = self._data.get('picked_by')
    self.round_pick_number = self._get_round_pick_number()
    self.player = self._get_player()
    self.team = self._get_pick_team()
    self.user = self.team.user if self.team else None
    self.team_name = self.team.team_name if self.team else str(self.picked_by)
    self.round = self._data.get('round')

  def __str__(self):
    return f"Round: {self.round} Pick: {self.round_pick_number} (Overall {self.pick_no}) by {self.team_name}"

  def _get_player(self) -> Player:
    return Player(self.player_id, self.player_data)

  def _get_round_pick_number(self) -> int:
    return ((self.pick_no - 1) % len(self._league_teams_by_user_id)) + 1

  def _get_pick_team(self) -> "Team | None":
    return self._league_teams_by_user_id.get(self.picked_by)
