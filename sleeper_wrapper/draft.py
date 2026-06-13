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
    self._data = self._get_draft()
    self.last_pick_time = datetime.fromtimestamp(self._data.get('last_picked') / 1000)
    self.draft_start_time = datetime.fromtimestamp(self._data.get('start_time') / 1000)
    self.draft_type = self._data.get('type')
    self.scoring_type = self._data.get('metadata').get('scoring_type')
  def __str__(self):
    return f"{self.draft_type} type draft {self.draft_id} started {self.draft_start_time}, last pick {self.last_pick_time}"

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
      roster_id = p.team_name
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
