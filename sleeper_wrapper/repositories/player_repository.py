# repositories/player_repository.py
"""Repository for looking up players, with optional local file caching."""

from __future__ import annotations

from typing import Any

from ..api_client import SleeperApiClient
from ..models.player import Player
from .file_cache import FileCache


class PlayerRepository:
  """Load player data and return Player objects by id."""

  def __init__(
    self,
    client: SleeperApiClient,
    sport: str,
    season: int,
    cache: FileCache | None = None,
  ) -> None:
    self.client = client
    self.sport = sport
    self.season = season
    self.cache = cache or FileCache(f"players_{sport}_{season}.json")
    self._players_by_id: dict[str, Player] | None = None

  def load_players_by_id(self) -> dict[str, Player]:
    """Return player payloads keyed by player id."""
    if self._players_by_id is not None:
      return self._players_by_id

    data = self.cache.read_or_none()
    if data is None:
      data = self.client.get_players(self.sport, str(self.season))
      self.cache.write_json(data)

    self._players_by_id = {
        str(player.get("player_id")): Player(player.get('player_id'), player)
        for player in data
        if isinstance(player, dict) and player.get("player_id") is not None
      }
    return self._players_by_id

  def get_player(self, player_id: int | str) -> Player:
    """Return a Player object for the given id."""
    player_id = str(player_id)
    players_by_id = self.load_players_by_id()
    player = players_by_id.get(player_id, {})
    return player
