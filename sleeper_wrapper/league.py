"""League model and related fetch helpers."""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from .base_api import BaseApi

if TYPE_CHECKING:
  from .draft import Draft
  from .matchup import Matchup
  from .team import Team
  from .transaction import Transaction
  from .user import User


class League(BaseApi):
  """Represent a Sleeper league."""

  def __init__(self, league_id: int) -> None:
    """Initialize a league.

    Args:
      league_id: League id to load.
    """
    self.league_id = int(league_id)
    self._data = self._get_data()

    self.season = self._data.get('season')
    self.sport = self._data.get('sport')
    self.settings = self._data.get('settings') or {}
    self.scoring_settings = self._data.get('scoring_settings') or {}
    self.first_week = self.settings.get('start_week')
    self.most_recent_week = self.settings.get('last_scored_leg')
    self.playoff_start = self.settings.get('playoff_week_start')
    self.num_teams = self._data.get('total_rosters')
    self.league_status = self._data.get('status')
    self.league_name = self._data.get('name')
    self.roster_positions = self._data.get('roster_positions')

    self.users: list["User"] = []
    self.users_by_id: dict[int, "User"] = {}
    self.teams: list["Team"] = []
    self.teams_by_user_id: dict[int, "Team"] = {}
    self.teams_by_roster_id: dict[int, "Team"] = {}
    self.drafts: list["Draft"] = []
    self.all_players = None
    self.sport_state = {}
    self.is_current_season = 0
    self.transactions: dict[int, list["Transaction"]] = {}

    from .assembler import LeagueAssembler

    LeagueAssembler().assemble_league(self)

  def __str__(self):
    """Return a readable league summary."""
    return f"{self.num_teams} Team League: {self.league_name} (ID {self.league_id})"

  def _get_data(self) -> dict:
    """Fetch league metadata.

    Returns:
      League payload.
    """
    return self.get_client().get_league(self.league_id)

  def get_results(self) -> dict[int, list["Matchup"]]:
    """Fetch matchups for all scored weeks.

    Returns:
      Matchups keyed by week.
    """
    r = defaultdict()
    if self.first_week is None or self.most_recent_week is None:
      return r

    for week in range(self.first_week, self.most_recent_week + 1):
      r[week] = self.get_week_matchups(week)
    return r

  def get_week_matchups(self, week: int) -> list["Matchup"]:
    """Fetch matchups for a week.

    Args:
      week: Week number to load.

    Returns:
      Matchup objects for the week.
    """
    from .assembler import LeagueAssembler

    return LeagueAssembler().assemble_week_matchups(self, week)

  def _get_transactions(self, week: int, transaction_type: str = "All") -> list["Transaction"]:
    """Fetch filtered transactions for a week.

    Args:
      week: Week number to load.
      transaction_type: Transaction type to include, or "All".

    Returns:
      Matching transaction objects.
    """
    from .assembler import LeagueAssembler

    if week not in self.transactions:
      self.transactions[week] = LeagueAssembler().assemble_transactions(self, week)

    return [t for t in self.transactions[week] if transaction_type in [t.transaction_type, "All"]]

  def get_all_transactions(self, week: int) -> list["Transaction"]:
    """Fetch all transactions for a week.

    Args:
      week: Week number to load.

    Returns:
      All transaction objects.
    """
    return self._get_transactions(week)

  def get_trades(self, week: int) -> list:
    """Fetch trade transactions for a week.

    Args:
      week: Week number to load.

    Returns:
      Trade transactions.
    """
    return self._get_transactions(week, "trade")

  def get_waivers(self, week: int) -> list:
    """Fetch waiver transactions for a week.

    Args:
      week: Week number to load.

    Returns:
      Waiver transactions.
    """
    return self._get_transactions(week, "waiver")

  def get_free_agents(self, week: int) -> list:
    """Fetch free agent transactions for a week.

    Args:
      week: Week number to load.

    Returns:
      Free agent transactions.
    """
    return self._get_transactions(week, "free_agent")
