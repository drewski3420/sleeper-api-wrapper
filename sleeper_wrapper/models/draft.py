"""Draft Model for League"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Draft:
  draft_id: int
  draft_data: dict | None = None
  _data: dict = field(init=False, repr=False)
  season: int | None = field(init=False)
  status: str | None = field(init=False)
  settings: dict = field(init=False)
  metadata: dict = field(init=False)
  league_id: int = field(init=False)
  sport: str = field(init=False)
  draft_type: str = field(init=False)
  slot_to_roster_id: dict = field(init=False)
  picks: list = field(init=False)
  traded_picks: list = field(init=False)
  teams: list = field(init=False)

  def __post_init__(self) -> None:
    self.draft_id = int(self.draft_id)
    self._data = self.draft_data or {}

    self.season = self._data.get("season")
    self.status = self._data.get("status")
    self.settings = self._data.get("settings") or {}
    self.metadata = self._data.get("metadata") or {}
    self.scoring_type = self.metadata.get("scoring_type") or "std"
    self.league_id = self._data.get("league_id")
    self.sport = self._data.get("sport")
    self.draft_type = self._data.get("type")
    self.slot_to_roster_id = self._data.get("slot_to_roster_id") or {}

    self.picks = []
    self.traded_picks = []
    self.teams = []

  def __str__(self) -> str:
    return f"Draft: {self.draft_id}"
