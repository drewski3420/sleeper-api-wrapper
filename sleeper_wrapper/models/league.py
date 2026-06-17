# models/league.py

from __future__ import annotations


class League:
  def __init__(self, league_data: dict | None = None) -> None:
    self._data = league_data or {}

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

  def __str__(self):
    return f"League: {self.league_name} (ID: {self.league_id})"
