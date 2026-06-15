from .user import User


class Team:
  def __init__(self, data: dict):
    self._data = data
    self.roster_id = int(self._data.get('roster_id'))
    self.user_obj: User | None = self._data.get('user_obj')
    self.team_name = self._get_team_name()

  def _get_team_name(self) -> str:
    if self.user_obj is None:
      return f"Roster {self.roster_id}"

    return self.user_obj.metadata.get('team_name') or self.user_obj.display_name

  def __str__(self):
    if self.user is None:
      return f"Team {self.team_name}"

    return f"Team {self.team_name} owned by {self.user_obj.display_name}"
