# models/league.py

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class League:
  league_data: dict | None = None
  _data: dict = field(init=False, repr=False)

  league_id: int = field(init=False)
  season: str | None = field(init=False)
  sport: str | None = field(init=False)
  settings: dict = field(init=False)
  scoring_settings: dict = field(init=False)
  first_week: int | None = field(init=False)
  most_recent_week: int | None = field(init=False)
  playoff_start: int | None = field(init=False)
  num_teams: int | None = field(init=False)
  league_status: str | None = field(init=False)
  league_name: str | None = field(init=False)
  roster_positions: list | None = field(init=False)

  users: list = field(init=False)
  users_by_id: dict = field(init=False)
  teams: list = field(init=False)
  teams_by_user_id: dict = field(init=False)
  teams_by_roster_id: dict = field(init=False)
  drafts: list = field(init=False)
  all_players: object | None = field(init=False)
  sport_state: dict = field(init=False)
  is_current_season: int = field(init=False)
  transactions: dict = field(init=False)
  trades: dict = field(init=False)
  free_agents: dict = field(init=False)
  waiver: dict = field(init=False)
  matchups: dict = field(init=False)

  def __post_init__(self) -> None:
    self._data = self.league_data or {}

    self.league_id = int(self._data.get("league_id"))
    self.season = self._data.get("season")
    self.sport = self._data.get("sport")
    self.settings = self._data.get("settings") or {}
    self.scoring_settings = self._data.get("scoring_settings") or {}
    self.first_week = self.settings.get("start_week")
    self.most_recent_week = self.settings.get("last_scored_leg")
    self.playoff_start = self.settings.get("playoff_week_start")
    self.num_teams = self._data.get("total_rosters")
    self.league_status = self._data.get("status")
    self.league_name = self._data.get("name")
    self.roster_positions = self._data.get("roster_positions")

    self.users = []
    self.users_by_id = {}
    self.teams = []
    self.teams_by_user_id = {}
    self.teams_by_roster_id = {}
    self.drafts = []
    self.all_players = None
    self.sport_state = {}
    self.is_current_season = 0
    self.transactions = {}
    self.trades = {}
    self.free_agents = {}
    self.waiver = {}
    self.matchups = {}

  def __str__(self) -> str:
    return f"League: {self.league_name} (ID: {self.league_id})"
