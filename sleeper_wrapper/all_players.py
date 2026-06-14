import json
import logging
import os
from typing import Any

from .base_api import BaseApi
from .player import Player

logger = logging.getLogger(__name__)


class AllPlayers(BaseApi):
  _cache: dict[tuple[str, int], dict[str, dict[str, Any]]] = {}

  def __init__(self, season: int, sport: str):
    self._sport = sport
    self._season = season
    self._cache_key = (self._sport, self._season)
    self._filename = f"players_{self._sport}_{self._season}.json"

    if self._cache_key not in AllPlayers._cache:
      AllPlayers._cache[self._cache_key] = self._get_contents(skip_check=False)

    self.players_by_id = AllPlayers._cache[self._cache_key]

  def _get_contents(self, skip_check: bool) -> dict[str, dict[str, Any]]:
    if not os.path.exists(self._filename) or skip_check:
      self._populate_file()

    with open(self._filename, 'r') as f:
      return json.loads(f.read())

  def _populate_file(self) -> None:
    data = self.get_client().get_players(self._sport)

    with open(self._filename, 'w') as f:
      f.write(json.dumps(data, indent=2))

  def get_player(self, player_id: int | str) -> Player:
    player_id = str(player_id)
    player_data = self.players_by_id.get(player_id)

    if player_data is None:
      logger.warning("Player id %s not found for sport=%s season=%s", player_id, self._sport, self._season)
      return Player(player_id, {})

    normalized_player_data = {
      **player_data,
      "stats": player_data.get("stats"),
    }
    return Player(player_id, normalized_player_data)

  def get_top_available(self, already_drafted_ids: list[int], sort_by: str, position: list[str] = ["All"]) -> list[Player]:
    limit = 40
    drafted_player_ids = {str(player_id) for player_id in already_drafted_ids}
    sort_field = f"adp_{sort_by}"
    available_players: list[Player] = []

    ranked_players = []
    for player_id, player_data in self.players_by_id.items():
      stats = player_data.get("stats") or {}
      ranked_val = (
        stats.get(sort_field)
        or stats.get("adp_std")
        or float("inf")
      )
      ranked_players.append((ranked_val, player_id, player_data))

    ranked_players.sort(key=lambda player: player[0])

    for _, player_id, player_data in ranked_players:
      if player_id in drafted_player_ids:
        continue

      player = Player(
        player_id=player_id,
        player_data={
          **player_data,
          "stats": player_data.get("stats"),
        },
      )

      if position[0] == 'All' or player.position in position:
        available_players.append(player)

      if len(available_players) >= limit:
        break

    return available_players
