# models/all_players.py
"""Player collection wrapper using a repository."""

from __future__ import annotations

from typing import Any

from ..api_client import SleeperApiClient
from ..models.player import Player
from ..repositories.file_cache import FileCache
from ..repositories.player_repository import PlayerRepository


class AllPlayers:
  """Load and cache all players for a sport and season."""

  def __init__(
    self,
    season: int,
    sport: str,
    client: SleeperApiClient | None = None,
    cache: FileCache | None = None,
  ) -> None:
    self._sport = sport
    self._season = season
    self.repository = PlayerRepository(
      client=client or SleeperApiClient(),
      sport=sport,
      season=season,
      cache=cache,
    )

  @property
  def players_by_id(self) -> dict[str, dict[str, Any]]:
    return self.repository.load_players_by_id()

  def get_player(self, player_id: int | str) -> Player:
    return self.repository.get_player(player_id)
