# models/draft.py

from __future__ import annotations


class Draft:
  def __init__(self, draft_id: int, draft_data: dict | None = None) -> None:
    self.draft_id = int(draft_id)
    self._data = draft_data or {}

    self.season = self._data.get("season")
    self.status = self._data.get("status")
    self.settings = self._data.get("settings") or {}
    self.metadata = self._data.get("metadata") or {}
    self.picks = []
    self.traded_picks = []
    self.teams = []

  def __str__(self):
    return f"Draft: {self.draft_id}"
