from datetime import datetime
from typing import TYPE_CHECKING

from .base_api import BaseApi
from .pick import Pick

if TYPE_CHECKING:
  from .team import Team
  from .user import User


class Draft(BaseApi):
  def __init__(
      self,
      draft_id: int,
      users_by_id: dict[int, "User"],
      teams_by_user_id: dict[int, "Team"],
  ) -> None:
    self.draft_id = int(draft_id)
    self._users_by_id = users_by_id
    self._teams_by_user_id = teams_by_user_id

    self.picks = self._get_all_picks()
    self._data = self._get_draft()

    last_picked = self._data.get('last_picked')
    start_time = self._data.get('start_time')
    metadata = self._data.get('metadata') or {}

    self.last_pick_time = datetime.fromtimestamp(last_picked / 1000) if last_picked else None
    self.draft_start_time = datetime.fromtimestamp(start_time / 1000) if start_time else None
    self.draft_type = self._data.get('type')
    self.scoring_type = metadata.get('scoring_type')

  def __str__(self):
    return f"{self.draft_type} type draft {self.draft_id} started {self.draft_start_time}, last pick {self.last_pick_time}"

  def _get_draft(self) -> dict:
    return self.get_client().get_draft(self.draft_id)

  def _get_all_picks(self) -> list[Pick]:
    picks = self.get_client().get_draft_picks(self.draft_id)
    return [Pick(pick, self._users_by_id, self._teams_by_user_id) for pick in picks]

  def _get_traded_picks(self) -> list[Pick]:
    picks = self.get_client().get_draft_traded_picks(self.draft_id)
    return [Pick(pick, self._users_by_id, self._teams_by_user_id) for pick in picks]

  def get_roster_counts(self) -> dict[str | None, dict[str | None, int]]:
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
