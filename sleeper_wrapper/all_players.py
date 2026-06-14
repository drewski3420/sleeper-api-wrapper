import os
import logging
import json

from .base_api import BaseApi
from .player import Player

logger = logging.getLogger(__name__)

class AllPlayers(BaseApi):
  _cache = None

  def __init__(self, season: int, sport: str = "nfl"):
    self._sport = sport
    self._season = season
    self._filenames = { "projections": {"fn":"projections.json", "endpoint": f"https://api.sleeper.app/v1/players/{self._sport}"}
                        , "players": {"fn":"players.json", "endpoint": f"https://api.sleeper.com/projections/{self._sport}/{self._season}?season_type=regular&order_by=adp_dynasty_ppr"}
                      }
    self.players = self._get_contents(type="players", skip_check=False )

    if AllPlayers._cache is None:
      AllPlayers._cache = self._get_contents("players", skip_check=False)
    self.players = AllPlayers._cache

  def _get_contents(self, type: str, skip_check: bool) -> Dict:
    fn = self._filenames[type]['fn']
    if not os.path.exists(fn) or skip_check:
      self._populate_file(type, fn)
    with open(fn,'r') as f:
      return json.loads(f.read())

  def _populate_file(self, type: str, fn: str) -> dict:
    url = self._filenames[type]['endpoint']
    with open(fn, 'w') as f:
      data = self._call(url)
      f.write(json.dumps(data))

#  def get_player(self, player_id: str | int) -> Player:
#    player_id = str(player_id)
#
#    metadata = self.players.get(player_id)
#
#    if metadata is None:
#      logger.warning(f"Player {player_id} not found")
#      return Player(player_id)
#
#    return Player(player_id, metadata)

  def get_top_available(self, already_drafted_ids: List[int], sort_by: str, position: List[str] = ["All"]) -> List[dict]:
    LIMIT = 40
    i = 0
    l = []
    sort_field = f"adp_{sort_by}"
    for player in self.players:
      player['stats']['ranked_val'] = (
        player["stats"].get(sort_field)
        or player["stats"].get("adp_std")
        or float("inf")
      )
    self.players.sort(key=lambda p: p["stats"]["ranked_val"])
    for player in self.players:
      if not player.get('player_id') in already_drafted_ids:
        player = Player(
          player_id=player.get('player_id'),
          player_data={ **player.get("player"), "stats": player.get("stats")}
        )
        if player.position in position or position[0] == 'All':
          l.append(player)
          i += 1
        if i >= LIMIT:
          break
    return l
