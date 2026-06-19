"""Player collection wrapper using a repository."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..api_client import SleeperApiClient
from ..models.player import Player
from ..repositories.file_cache import FileCache
from ..repositories.player_repository import PlayerRepository


@dataclass
class AllPlayers:
  """Load and cache all players for a sport and season."""

  season: int
  sport: str
  client: SleeperApiClient | None = None
  cache: FileCache | None = None
  repository: PlayerRepository = field(init=False)

  def __post_init__(self) -> None:
    self.repository = PlayerRepository(
      client=self.client or SleeperApiClient(),
      sport=self.sport,
      season=self.season,
      cache=self.cache,
    )

  @property
  def players_by_id(self) -> dict[str, Player]:
    return self.repository.load_players_by_id()

  def get_player(self, player_id: int | str) -> Player:
    return self.repository.get_player(player_id)
