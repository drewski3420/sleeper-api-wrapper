"""User-related service operations."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.draft import Draft
from ..models.league import League
from ..models.user import User


class UserService:
  """Load user-related aggregates from the API."""

  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()

  def load_user(self, user_name: str, user_data: dict | None = None) -> User:
    """Create a User from provided data, or fetch it if missing."""
    if user_data is None:
      user_data = self.client.get_user(user_name)
    return User(user_name, user_data)

  def get_all_leagues(self, user_id: int, season: int, sport: str) -> list[League]:
    """Fetch all leagues for a user."""
    leagues = self.client.get_user_leagues(user_id, sport, season)
    return [League(int(league["league_id"]), league) for league in leagues]

  def get_all_drafts(self, user_id: int, season: int, sport: str) -> list[Draft]:
    """Fetch all drafts for a user."""
    drafts = self.client.get_user_drafts(user_id, sport, season)
    return [Draft(int(draft["draft_id"]), draft) for draft in drafts]
