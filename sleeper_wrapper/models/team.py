"""Team model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .user import User


@dataclass
class Team:
  """Represent a league roster/team."""

  data: dict
  _data: dict = field(init=False, repr=False)
  roster_id: int = field(init=False)
  user_obj: User | None = field(init=False)
  team_name: str = field(init=False)

  def __post_init__(self) -> None:
    """Initialize derived team fields."""
    self._data = self.data
    self.roster_id = int(self._data.get("roster_id"))
    self.user_obj = self._data.get("user_obj")
    self.team_name = self._get_team_name()

  def _get_team_name(self) -> str:
    """Resolve the display name for the team.

    Returns:
      Team display name.
    """
    if self.user_obj is None:
      return f"Roster {self.roster_id}"

    return self.user_obj.metadata.get("team_name") or self.user_obj.display_name

  def __str__(self) -> str:
    """Return a readable team summary."""
    if self.user_obj is None:
      return f"Team {self.team_name}"

    return f"Team {self.team_name} owned by {self.user_obj.display_name}"
