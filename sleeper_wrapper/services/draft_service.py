"""Draft-related service operations."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.draft import Draft
from ..models.pick import Pick, TradedPick
from ..models.team import Team
from ..models.user import User
from ..models.all_players import AllPlayers
#from ..models.player import Player

class DraftService:
  """Load draft-related aggregates from the API."""

  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()

  def load_draft(self, draft_id: int, draft_data: dict | None = None) -> Draft:
    """Create a Draft from provided data, or fetch it if missing."""
    if draft_data is None:
      draft_data = self.client.get_draft(draft_id)
    return Draft(draft_id, draft_data)

  def get_all_picks(self, draft: Draft) -> list[Pick]:
    """Fetch and build all picks for a draft."""
    users_by_id, teams_by_user_id, _teams_by_roster_id = self._get_draft_context(draft)
    raw_picks = self.client.get_draft_picks(draft.draft_id)
    return [Pick(pick, users_by_id, teams_by_user_id) for pick in raw_picks]

  def get_all_traded_picks(self, draft: Draft) -> list[TradedPick]:
    """Fetch and build traded picks for a draft."""
    _users_by_id, _teams_by_user_id, teams_by_roster_id = self._get_draft_context(draft)
    raw_picks = self.client.get_draft_traded_picks(draft.draft_id)
    return [TradedPick(pick, teams_by_roster_id) for pick in raw_picks]

  def get_top_available(self, draft: Draft, position: list[str] | str, num_to_return: int = 50) -> list[Player]:
    """Get top available players by ADP.

    Args:
      position: Positions to include.
      num_to_return: How many player to return, or 50

    Returns:
      Available players
    """
    if isinstance(position,str):
      position = [position]

    drafted_player_ids = {
      str(pick.player_id)
      for pick in self.get_all_picks(draft)
      if pick.player_id is not None
    }
    scoring_type = draft.scoring_type or "std"
    sort_field = f"adp_{scoring_type}"
    available_players: list[Player] = []
    ranked_players = []

    all_players = AllPlayers(season=draft.season, sport=draft.sport)
    for player_id, player in all_players.players_by_id.items():
      player_stats = player.stats or {}
      ranked_val = (
        player_stats.get(sort_field)
        or player_stats.get("adp_std")
        or float("inf")
      )
      ranked_players.append((ranked_val, player)) #player_id, player_data, player_stats))
    ranked_players.sort(key=lambda player: player[0])

    for ranked_val, player in ranked_players:
      if player_id in drafted_player_ids:
        continue
      if position[0] == 'All' or player.position in position:
        player.stats['ranked_val'] = ranked_val
        available_players.append(player)

      if len(available_players) >= num_to_return:
        break

    return available_players

  def _get_draft_context(
    self,
    draft: Draft,
  ) -> tuple[dict[int, User], dict[int, Team], dict[int, Team]]:
    """Build user and team lookup maps for a draft via its league."""
    league_id = draft.league_id
    if league_id is None:
      return {}, {}, {}

    users = self.client.get_league_users(int(league_id))
    user_objects = [
      User(int(user_data.get("user_id")), user_data=user_data)
      for user_data in users
    ]
    users_by_id = {user.user_id: user for user in user_objects}

    rosters = self.client.get_league_rosters(int(league_id))
    teams: list[Team] = []
    for roster_data in rosters:
      owner_id = roster_data.get("owner_id")
      roster_data = dict(roster_data)
      roster_data["user_obj"] = users_by_id.get(int(owner_id)) if owner_id is not None else None
      teams.append(Team(roster_data))

    teams_by_user_id = {
      team.user_obj.user_id: team
      for team in teams
      if team.user_obj is not None
    }
    teams_by_roster_id = {team.roster_id: team for team in teams}

    return users_by_id, teams_by_user_id, teams_by_roster_id
