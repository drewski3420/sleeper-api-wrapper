"""Team model."""

from .user import User

class Team:
  """Represent a league roster/team."""

  def __init__(self, data: dict):
    """Initialize a team.

    Args:
      data: Raw roster payload.
    """
    self._data = data
    self.roster_id = int(self._data.get('roster_id'))
    self.user_obj: User | None = self._data.get('user_obj')
    self.team_name = self._get_team_name()

  def _get_team_name(self) -> str:
    """Resolve the display name for the team.

    Returns:
      Team display name.
    """
    if self.user_obj is None:
      return f"Roster {self.roster_id}"

    return self.user_obj.metadata.get('team_name') or self.user_obj.display_name

  def __str__(self):
    """Return a readable team summary."""
    if self.user_obj is None:
      return f"Team {self.team_name}"

    return f"Team {self.team_name} owned by {self.user_obj.display_name}"
