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
      data = json.loads(f.read())
      return { f['player_id']: f for f in data}

  def _populate_file(self) -> None:
    data = self.get_client().get_players(self._sport, self._season)

    with open(self._filename, 'w') as f:
      f.write(json.dumps(data, indent=2))

  def get_player(self, player_id: int | str) -> Player:
    player_id = str(player_id)
    player_data = self.players_by_id.get(player_id)

    if player_data is None:
      logger.warning("Player id %s not found for sport=%s season=%s", player_id, self._sport, self._season)
      return Player(player_id, {})

    if "player" in player_data.keys():
      p = player_data.pop("player")
      player_data.update(p)

    return Player(
      player_id=player_id,
      player_data=player_data,
    )

