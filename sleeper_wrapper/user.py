"""User model and related fetch helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base_api import BaseApi

if TYPE_CHECKING:
  from .draft import Draft
  from .league import League


class User(BaseApi):
  """The data associated with a given Sleeper user."""

  def __init__(self, initial_user_input: int, user_data: dict | None = None) -> None:
    """Initialize a user.

    Args:
      initial_user_input: User id to load when user_data is not provided.
      user_data: Optional raw user payload.
    """
    self._data = user_data or self.get_client().get_user(initial_user_input)
    self.user_id = int(self._data.get('user_id'))
    self.username = self._data.get('username')
    self.display_name = self._data.get('display_name')
    self.metadata = self._data.get('metadata') or {}

  def __str__(self):
    """Return a readable user summary."""
    return f"User: {self.username} User ID: {self.user_id} Display Name: {self.display_name}"

  def _get_data(self, initial_user_input: int) -> dict:
    """Fetch user metadata.

    Args:
      initial_user_input: User id to load.

    Returns:
      User payload.
    """
    return self.get_client().get_user(initial_user_input)

  def get_all_leagues(self, season: int, sport: str) -> list["League"]:
    """Fetch all leagues for the user.

    Args:
      season: Season year to query.
      sport: Sport key to query.

    Returns:
      League objects for the user.
    """
    from .league import League

    leagues = self.get_client().get_user_leagues(self.user_id, sport, season)
    return [League(int(l.get('league_id'))) for l in leagues]

  def get_all_drafts(self, season: int, sport: str) -> list["Draft"]:
    """Fetch all drafts for the user.

    Args:
      season: Season year to query.
      sport: Sport key to query.

    Returns:
      Draft objects for the user.
    """
    from .draft import Draft

    drafts = self.get_client().get_user_drafts(self.user_id, sport, season)
    return [Draft(int(d.get('draft_id')), {self.user_id: self}, {}) for d in drafts]
