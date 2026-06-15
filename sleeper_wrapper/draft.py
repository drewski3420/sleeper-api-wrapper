"""Draft models and helpers."""

from datetime import datetime
from typing import TYPE_CHECKING

from .all_players import AllPlayers
from .base_api import BaseApi
from .pick import Pick
from .player import Player

if TYPE_CHECKING:
  from .team import Team
  from .user import User


class Draft(BaseApi):
  """Represent a Sleeper draft."""

  def __init__(
      self,
      draft_id: int,
      users_by_id: dict[int, "User"],
      teams_by_user_id: dict[int, "Team"],
      all_players: AllPlayers,
  ) -> None:
    """Initialize a draft.

    Args:
      draft_id: Draft id to load.
      users_by_id: User mapping keyed by user id.
      teams_by_user_id: Team mapping keyed by user id.
      all_players: Player lookup helper.
    """
    self.draft_id = int(draft_id)
    self._users_by_id = users_by_id
    self._teams_by_user_id = teams_by_user_id
    self._all_players = all_players

    self.picks = self._get_all_picks()
    self.traded_picks = self._get_traded_picks()
    self._data = self._get_draft()

    last_picked = self._data.get('last_picked')
    start_time = self._data.get('start_time')
    metadata = self._data.get('metadata') or {}

    self.last_pick_time = datetime.fromtimestamp(last_picked / 1000) if last_picked else None
    self.draft_start_time = datetime.fromtimestamp(start_time / 1000) if start_time else None
    self.draft_type = self._data.get('type')
    self.type = self.draft_type
    self.scoring_type = metadata.get('scoring_type')
    self.season = self._data.get('season')
    self.sport = self._data.get('sport') or "nfl"

  def __str__(self):
    """Return a readable draft summary."""
    return f"{self.draft_type} type draft {self.draft_id} started {self.draft_start_time}, last pick {self.last_pick_time}"

  def _get_draft(self) -> dict:
    """Fetch draft metadata.

    Returns:
      Draft payload.
    """
    return self.get_client().get_draft(self.draft_id)

  def _get_all_picks(self) -> list[Pick]:
    """Fetch all picks for the draft.

    Returns:
      Pick objects for the draft.
    """
    picks = self.get_client().get_draft_picks(self.draft_id)
    return [Pick(pick, self._users_by_id, self._teams_by_user_id) for pick in picks]

  def _get_traded_picks(self) -> list[Pick]:
    """Fetch traded picks for the draft.

    Returns:
      Pick objects for traded picks.
    """
    picks = self.get_client().get_draft_traded_picks(self.draft_id)
    return [Pick(pick, self._users_by_id, self._teams_by_user_id) for pick in picks]

  def get_top_available(self, position: list[str] = ["All"]) -> list[Player]:
    """Get top available players by ADP.

    Args:
      position: Positions to include, or ["All"].

    Returns:
      Up to 40 available players.
    """
    drafted_player_ids = {
      str(pick.player_id)
      for pick in self.picks
      if pick.player_id is not None
    }
    scoring_type = self.scoring_type or "std"
    sort_field = f"adp_{scoring_type}"
    available_players: list[Player] = []
    ranked_players = []

    for player_id, player_data in self._all_players.players_by_id.items():
      player_stats = player_data['stats'] or {}
      ranked_val = (
        player_stats.get(sort_field)
        or player_stats.get("adp_std")
        or float("inf")
      )
      ranked_players.append((ranked_val, str(player_id), player_data, player_stats))

    ranked_players.sort(key=lambda player: player[0])

    for ranked_val, player_id, player_data, player_stats in ranked_players:
      if player_id in drafted_player_ids:
        continue
      player_stats['ranked_val'] = ranked_val

      p = player_data.pop("player")
      player_data.update(p)

      player = Player(
        player_id=player_id,
        player_data=player_data,
      )

      if position[0] == 'All' or player.position in position:
        available_players.append(player)

      if len(available_players) >= 40:
        break

    return available_players

  def get_roster_counts(self) -> dict[str | None, dict[str | None, int]]:
    """Count drafted positions by roster.

    Returns:
      Nested counts keyed by team name and position.
    """
    counts = {}

    for p in self.picks:
      roster_id = p.team_name
      position = p.player_obj.position

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
