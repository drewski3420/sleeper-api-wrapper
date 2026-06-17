# services/matchup_service.py
"""Service for loading matchups."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.matchup import Matchup


class MatchupService:
  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()

  def load_week_matchups(self, league_id: int, week: int) -> list[Matchup]:
    raw_matchups = self.client.get_week_matchups(league_id, week)
    return [Matchup.from_payload(matchup_id=int(k), data=v) for k, v in raw_matchups.items()]
