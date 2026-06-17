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
    self._players_by_id: dict[str, dict[str, Any]] | None = None

  def load_players_by_id(self) -> dict[str, dict[str, Any]]:
    """Return player payloads keyed by player id."""
    if self._players_by_id is not None:
      return self._players_by_id

    data = self.cache.read_or_none()
    if data is None:
      data = self.client.get_players(self.sport, str(self.season))
      self.cache.write_json(data)

    self._players_by_id = self._normalize_players(data)
    return self._players_by_id

  def _normalize_players(self, data: Any) -> dict[str, dict[str, Any]]:
    """Normalize API/cache payload into a player-id lookup."""
    if isinstance(data, dict):
      return {str(player_id): player_data for player_id, player_data in data.items()}

    return {
      str(player.get("player_id")): player
      for player in data
      if isinstance(player, dict) and player.get("player_id") is not None
    }

  def get_player(self, player_id: int | str) -> Player:
    """Return a Player object for the given id."""
    player_id = str(player_id)
    players_by_id = self.load_players_by_id()
    player_data = players_by_id.get(player_id, {})
    return Player(player_id, player_data)
