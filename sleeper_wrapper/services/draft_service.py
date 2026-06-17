"""Draft-related service operations."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.draft import Draft
from ..models.pick import Pick
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
    raw_picks = self.client.get_draft_picks(draft_id)
    return [Pick(pick, {}, {}) for pick in raw_picks]

  def get_traded_picks(self, draft_id: int) -> list[Pick]:
    """Fetch and build traded picks for a draft."""
    raw_picks = self.client.get_draft_traded_picks(draft_id)
    return [Pick(pick, {}, {}) for pick in raw_picks]
