"""Service for loading and populating leagues."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.league import League
from .league_assembler import LeagueAssembler


class LeagueService:
  """Load league data and assemble related objects."""

  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()
    self.assembler = LeagueAssembler()

  def load_league(self, league_id: int) -> League:
    """Fetch a league and populate its related objects."""
    league_data = self.client.get_league(league_id)
    league = League(league_data)
    self.assembler.assemble_league(league)
    return league

  def get_week_matchups(self, league: League, week: int):
    """Load matchups for a given week."""
    return self.assembler.assemble_week_matchups(league, week)

  def get_week_transactions(self, league: League, week: int):
    if week not in league.transactions:
      league.transactions[week] = self.assembler.assemble_week_transactions(league, week)
    return league.transactions[week]

  def get_week_trades(self, league: League, week: int):
    transactions = self.get_week_transactions(league, week)
    return [t for t in transactions if t.transaction_type == "trade"]

  def get_week_waivers(self, league: League, week: int):
    transactions = self.get_week_transactions(league, week)
    return [t for t in transactions if t.transaction_type == "waiver"]

  def get_week_free_agent(self, league: League, week: int):
    transactions = self.get_week_transactions(league, week)
    return [t for t in transactions if t.transaction_type == "free_agent"]
