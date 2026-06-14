from __future__ import annotations

from typing import TYPE_CHECKING

from .base_api import BaseApi

if TYPE_CHECKING:
  from .draft import Draft
  from .league import League


class User(BaseApi):
  """The data associated with a given Sleeper user."""

  def __init__(self, initial_user_input: int, user_data: dict | None = None) -> None:
    self._data = user_data or self.get_client().get_user(initial_user_input)
    self.user_id = self._data.get('user_id')
    self.username = self._data.get('username')
    self.display_name = self._data.get('display_name')
    self.metadata = self._data.get('metadata') or {}

  def __str__(self):
    return f"User: {self.username} User ID: {self.user_id} Display Name: {self.display_name}"

  def _get_data(self, initial_user_input: int) -> dict:
    return self.get_client().get_user(initial_user_input)

  def get_all_leagues(self, season: int, sport: str = "nfl") -> list["League"]:
    from .league import League

    leagues = self.get_client().get_user_leagues(self.user_id, sport, season)
    return [League(l.get('league_id')) for l in leagues]

  def get_all_drafts(self, season: int, sport: str = "nfl") -> list["Draft"]:
    from .draft import Draft

    drafts = self.get_client().get_user_drafts(self.user_id, sport, season)
    return [Draft(d.get('draft_id'), {}) for d in drafts]
