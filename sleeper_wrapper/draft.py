from datetime import datetime
from typing import Union

from .base_api import BaseApi
from .pick import Pick
from .user import User

class Draft(BaseApi):
  def __init__(self, draft_id: Union[str, int], league_users: dict[int, User]) -> None:
    self.draft_id = draft_id
    self._league_users = league_users
    self._base_url = f"https://api.sleeper.app/v1/draft/{self.draft_id}"

    self.picks = self._get_all_picks()
    self.data = self._get_draft()
    self.__dict__.update(self.data)
    self.last_pick_time = datetime.fromtimestamp(self._data.get('last_picked') / 1000)
    self.draft_start_time = datetime.fromtimestamp(self._data.get('start_time') / 1000)

  def _get_draft(self) -> dict:
    return self._call(self._base_url)

  def _get_all_picks(self) -> list[Pick]:
    picks = self._call(f"{self._base_url}/picks")
    return [Pick(pick, self._league_users) for pick in picks]

  def _get_traded_picks(self) -> list[Pick]:
    picks = self._call(f"{self._base_url}/traded_picks")
    return [Pick(pick) for pick in picks]

  def get_roster_counts(self) -> dict[str, dict[str, int]]:
    counts = {}

    for p in self.picks:
#      for team_name, pick in p.items():
        #print(f"Round {pick.round} Pick {pick.round_pick_number}: {pick.player.full_name} ({pick.player.position}, Year: {pick.player.years_exp})")
      roster_id = p.team_name #pick.roster_id
      position = p.player.position

      
      counts.setdefault(roster_id, {})
      counts[roster_id][position] = counts[roster_id].get(position, 0) + 1

    return counts
#  def roster_contruction(self) -> Dict:
#
#      counts = self.construction_counts()
#      order = ["QB", "RB", "WR", "TE"]
#      parts = [f"{counts.get(pos, 0)} {pos}" for pos in order]
#
#      other_positions = sorted(pos for pos in counts if pos not in order)
#      parts.extend(f"{counts[pos]} {pos}" for pos in other_positions)
#
#      return " / ".join(parts)
#
##  def _update_draft_order(self) -> list[tuple[int, int]]:
##    return [
##      (position, user_id)
##      for user_id, position in sorted(self.draft_order.items(), key=lambda x: x[1])
##    ]
