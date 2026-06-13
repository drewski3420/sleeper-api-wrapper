
from typing import Union

from .base_api import BaseApi
from .all_players import AllPlayers
from .user import User
#from .player import Player

class Team:
  def __init__(self, data: dict):
#    print(data)
    self.__dict__.update(data) #expand all properties
    self.roster = [
      players.get_player(pid)
      for pid in (data.get('players') or [])
    ]
#    all_players = Players()
#    self.players = self._get_players()

#  def _get_players(self) -> List[Player]:
#    print(self.players)
#    return [Player(player) for player in self.players]
#
#  def _get_player(self, player_info: dict) -> Player:
#    return Player(player_info)

#  def _get_round_pick_number(self, overall_pick: int) -> int:
#    return ((overall_pick - 1) % 8) + 1

#class Drew_Roster:
#    roster_id: int
#    picks: List[Drew_Pick] = field(default_factory=list)
#
#    def add_pick(self, pick: Drew_Pick) -> None:
#        self.picks.append(pick)
#
#    def construction_counts(self) -> Dict[str, int]:
#        return dict(Counter(p.position.upper() for p in self.picks))
#
#    def construction(self) -> str:
#        counts = self.construction_counts()
#        order = ["QB", "RB", "WR", "TE"]
#        parts = [f"{counts.get(pos, 0)} {pos}" for pos in order]
#
#        other_positions = sorted(pos for pos in counts if pos not in order)
#        parts.extend(f"{counts[pos]} {pos}" for pos in other_positions)
#
#        return " / ".join(parts)
