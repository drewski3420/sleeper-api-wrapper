from typing import List

from .base_api import BaseApi
from .player import Player
from .team import Team

"""
{'points': 133.66, 
'players': ['11563', '11581', '11618', '11632', '11635', '12469', '12505', '12508', '12512', '12518', '3214', '4137', '4663', '4950', '4984', '5947', '6783', '6803', '7528', '8131', '8150', '8183', '9228', '9484', '9488', '9508'], 
'roster_id': 7, 'custom_points': None, 
'matchup_id': 1, 
'starters': ['4984', '8150', '4137', '11632', '11635', '9488', '12518', '5947', '6783'], 
'starters_points': [38.76, 13.4, 12.4, 9.6, 10.4, 14.9, 11.4, 13.7, 9.1], 
'players_points': {'11563': 6.84, '11581': 0.0, '11618': 0.0, '11632': 9.6, '11635': 10.4, '12469': 13.3, '12505': 0.0, '12508': 0.0, '12512': 0.0, '12518': 11.4, '3214': 8.6, '4137': 12.4, '4663': 7.2, '4950': 0.0, '4984': 38.76, '5947': 13.7, '6783': 9.1, '6803': 0.0, '7528': 1.5, '8131': 0.0, '8150': 13.4, '8183': 16.78, '9228': 8.16, '9484': 8.9, '9488': 14.9, '9508': 0.0}
}
"""
class TeamEntry:
  def __init__(self, data: dict):
    self._data = data
    self.roster_id = self._data["roster_id"]
    self.points = self._data["points"]
    self.players_with_points = self._get_player_points()
    self.starter_points = sum(d["points"] for d in self.players_with_points if d["is_starter"] == 1)
    self.bench_points = sum(d["points"] for d in self.players_with_points if d["is_bench"] == 1)
    self.matchup_id = self._data["matchup_id"]
    self.team_obj = None
    
  def _get_player_points(self) -> List:
    players_points = self._data["players_points"]
    starters = self._data["starters"]
    r = []
    for player_id, points in players_points.items():
      p = {}
      p['player_id'] = player_id
      p['points'] = points
      p['is_starter'] = (1 if player_id in starters else 0)
      p['is_bench'] = (1 if player_id not in starters else 0)
      p['player'] = None
      r.append(p)
    return r

  def __str__(self):
    return str(self.__dict__)

class Matchup:
  def __init__(self, matchup_id: int, data: List):
    self._data = data
    self.matchup_id = matchup_id
    self.teams = [TeamEntry(e) for e in data]
    self.winning_roster_id = None
    self.losing_roster_id = None
    self.winning_team = None
    self.losing_team = None
    self._determine_outcome()

  def _determine_outcome(self) -> None:
    t1 = self.teams[0]
    t2 = self.teams[1]
    if t1.points > t2.points:
      self.winning_roster_id = t1.roster_id
      self.losing_roster_id = t2.roster_id
      self.winning_team = t1
      self.losing_team = t2
    else:
      self.winning_roster_id = t2.roster_id
      self.losing_roster_id = t1.roster_id
      self.winning_team = t2
      self.losing_team = t1

  def __str__(self):
    return f"Matchup Number: {str(self.matchup_id)} - " + (" def. ".join([f"{t.team_obj.team_name} ({t.points})" for t in [self.winning_team, self.losing_team]]))
