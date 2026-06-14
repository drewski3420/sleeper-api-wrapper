from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Union

from .base_api import BaseApi

if TYPE_CHECKING:
  from .draft import Draft
  from .matchup import Matchup
  from .team import Team
  from .transaction import Transaction


class League(BaseApi):
  def __init__(self, league_id: Union[str, int]) -> None:
    self.league_id = league_id
    self._data = self._get_data()

    self.season = self._data.get('season')
    self.sport = self._data.get('sport')
    self.settings = self._data.get('settings')
    self.scoring_settings = self._data.get('scoring_settings')
    self.first_week = self.settings.get('start_week')
    self.most_recent_week = self.settings.get('last_scored_leg')
    self.playoff_start = self.settings.get('playoff_week_start')
    self.num_teams = self._data.get('total_rosters')
    self.league_status = self._data.get('status')
    self.league_name = self._data.get('name')

    self.users = []
    self.users_by_id = {}
    self.teams = []
    self.teams_by_user_id = {}
    self.teams_by_roster_id = {}
    self.drafts: list["Draft"] = []
    self.all_players = None
    self.sport_state = {}
    self.is_current_season = 0
    self.transactions: dict[int, list["Transaction"]] = {}

    from .league_assembler import LeagueAssembler

    LeagueAssembler(self.get_client()).assemble_league(self)

  def __str__(self):
    return f"{self.num_teams} Team League: {self.league_name} (ID {self.league_id})"

  def _get_data(self) -> dict:
    return self.get_client().get_league(self.league_id)

  def get_results(self) -> dict[int, list["Matchup"]]:
    r = defaultdict()
    for week in range(self.first_week, self.most_recent_week + 1):
      r[week] = self.get_week_matchups(week)
    return r

  def get_week_matchups(self, week: int) -> list["Matchup"]:
    from .league_assembler import LeagueAssembler

    return LeagueAssembler(self.get_client()).assemble_week_matchups(self, week)

  def _get_transactions(self, week: int, transaction_type: str = "All") -> list["Transaction"]:
    from .league_assembler import LeagueAssembler

    if week not in self.transactions:
      self.transactions[week] = LeagueAssembler(self.get_client()).assemble_transactions(self, week)

    return [t for t in self.transactions[week] if transaction_type in [t.transaction_type, "All"]]

  def get_trades(self, week: int) -> list:
    return self._get_transactions(week, "trade")

  def get_waivers(self, week: int) -> list:
    return self._get_transactions(week, "waiver")

  def get_free_agents(self, week: int) -> list:
    return self._get_transactions(week, "free_agent")
