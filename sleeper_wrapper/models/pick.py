"""Draft pick model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .player import Player

if TYPE_CHECKING:
  from .team import Team
  from .user import User


class Pick:
  """Represent a draft pick."""

  def __init__(
    self,
    data: dict,
    users_by_id: dict[int, "User"],
    teams_by_user_id: dict[int, "Team"],
  ) -> None:
    """Initialize a draft pick.

    Args:
      data: Raw pick payload.
      users_by_id: User mapping keyed by user id.
      teams_by_user_id: Team mapping keyed by user id.
    """
    self._users_by_id = users_by_id
    self._teams_by_user_id = teams_by_user_id
    self._data = data

    self.pick_no = self._data.get("pick_no")
    self.round = self._data.get("round")

    self.metadata = self._data.get("metadata") or {}
    self.player_id = (
      str(self.metadata.get("player_id"))
      if self.metadata.get("player_id") is not None
      else None
    )

    picked_by = self._data.get("picked_by")
    self.picked_by_user_id = int(picked_by) if picked_by is not None else None

    self.round_pick_number = self._get_round_pick_number()
    self.player_obj = self._get_player()
    self.user_obj = self._get_pick_user()
    self.team_obj = self._get_pick_team()
    self.team_name = self.team_obj.team_name if self.team_obj else None

  def __str__(self) -> str:
    """Return a readable pick summary."""
    team_name = self.team_name or "Unknown team"
    return f"Round: {self.round} Pick: {self.round_pick_number} (Overall {self.pick_no}) by {team_name}"

  def _get_player(self) -> Player:
    """Build the picked player object."""
    return Player(self.player_id or "", self.metadata)

  def _get_round_pick_number(self) -> int:
    """Compute the pick number within the round."""
    team_count = len(self._teams_by_user_id)
    if team_count == 0 or self.pick_no is None:
      return 0
    return ((self.pick_no - 1) % team_count) + 1

  def _get_pick_user(self) -> "User | None":
    """Resolve the picking user."""
    if self.picked_by_user_id is None:
      return None
    return self._users_by_id.get(self.picked_by_user_id)

  def _get_pick_team(self) -> "Team | None":
    """Resolve the picking team."""
    if self.picked_by_user_id is None:
      return None
    return self._teams_by_user_id.get(self.picked_by_user_id)


class TradedPick:
  """Represent a traded draft-pick asset."""

  def __init__(
    self,
    data: dict,
    teams_by_roster_id: dict[int, "Team"],
  ) -> None:
    """Initialize a traded pick.

    Args:
      data: Raw traded-pick payload.
      teams_by_roster_id: Team mapping keyed by roster id.
    """
    self._data = data
    self._teams_by_roster_id = teams_by_roster_id

    self.season = str(self._data.get("season")) if self._data.get("season") is not None else None
    self.round = self._data.get("round")

    roster_id = self._data.get("roster_id")
    previous_owner_id = self._data.get("previous_owner_id")
    owner_id = self._data.get("owner_id")

    self.original_roster_id = int(roster_id) if roster_id is not None else None
    self.previous_owner_roster_id = (
      int(previous_owner_id) if previous_owner_id is not None else None
    )
    self.current_owner_roster_id = int(owner_id) if owner_id is not None else None

    self.original_owner_team_obj = self._get_team(self.original_roster_id)
    self.previous_owner_team_obj = self._get_team(self.previous_owner_roster_id)
    self.current_owner_team_obj = self._get_team(self.current_owner_roster_id)

  def __str__(self) -> str:
    """Return a readable traded-pick summary."""
    current_owner = (
      self.current_owner_team_obj.team_name
      if self.current_owner_team_obj is not None
      else f"Roster {self.current_owner_roster_id}"
      if self.current_owner_roster_id is not None
      else "Unknown roster"
    )
    return f"Season: {self.season} Round: {self.round} Current Owner: {current_owner}"

  def _get_team(self, roster_id: int | None) -> "Team | None":
    """Resolve a team by roster id."""
    if roster_id is None:
      return None
    return self._teams_by_roster_id.get(roster_id)
