"""Draft-related service operations."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.draft import Draft
from ..models.pick import Pick
from ..models.team import Team
from ..models.user import User


class DraftService:
  """Load draft-related aggregates from the API."""

  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()

  def load_draft(self, draft_id: int, draft_data: dict | None = None) -> Draft:
    """Create a Draft from provided data, or fetch it if missing."""
    if draft_data is None:
      draft_data = self.client.get_draft(draft_id)
    return Draft(draft_id, draft_data)

  def get_all_picks(self, draft_id: int) -> list[Pick]:
    """Fetch and build all picks for a draft."""
    draft = self.load_draft(draft_id)
    users_by_id, teams_by_user_id = self._get_draft_context(draft)
    raw_picks = self.client.get_draft_picks(draft_id)
    return [Pick(pick, users_by_id, teams_by_user_id) for pick in raw_picks]

  def get_traded_picks(self, draft_id: int) -> list[Pick]:
    """Fetch and build traded picks for a draft."""
    draft = self.load_draft(draft_id)
    users_by_id, teams_by_user_id = self._get_draft_context(draft)
    raw_picks = self.client.get_draft_traded_picks(draft_id)
    return [Pick(pick, users_by_id, teams_by_user_id) for pick in raw_picks]

  def _get_draft_context(self, draft: Draft) -> tuple[dict[int, User], dict[int, Team]]:
    """Build user and team lookup maps for a draft via its league."""
    league_id = draft._data.get("league_id")
    if league_id is None:
      return {}, {}

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

    return users_by_id, teams_by_user_id
