"""HTTP client for Sleeper API endpoints."""

from __future__ import annotations

from typing import Any

import requests


class SleeperApiClient:
  """Make requests to the Sleeper API."""

  def __init__(self, base_url: str = "https://api.sleeper.app/v1") -> None:
    """Initialize the API client.

    Args:
      base_url: Base API URL to use for requests.
    """
    self.base_url = base_url.rstrip("/")
    self.root_url = self.base_url.removesuffix("/v1")

  def get(self, url: str) -> Any:
    """Send a GET request.

    Args:
      url: Full URL to request.

    Returns:
      Parsed JSON response.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

  def get_by_path(self, path: str) -> Any:
    """Request an API path under the v1 base URL.

    Args:
      path: Path relative to the v1 API root.

    Returns:
      Parsed JSON response.
    """
    normalized_path = path.lstrip("/")
    return self.get(f"{self.base_url}/{normalized_path}")

  def get_by_root_path(self, path: str) -> Any:
    """Request a path under the non-v1 root URL.

    Args:
      path: Path relative to the API root.

    Returns:
      Parsed JSON response.
    """
    normalized_path = path.lstrip("/")
    return self.get(f"{self.root_url}/{normalized_path}")

  def get_user(self, user_input: int | str) -> dict:
    """Fetch a user.

    Args:
      user_input: User id or user name to request.

    Returns:
      User payload.
    """
    return self.get_by_path(f"user/{user_input}")

  def get_user_leagues(self, user_id: int, sport: str, season: int) -> list:
    """Fetch leagues for a user.

    Args:
      user_id: User id to request.
      sport: Sport key.
      season: Season year.

    Returns:
      League payloads.
    """
    return self.get_by_path(f"user/{user_id}/leagues/{sport}/{season}")

  def get_user_drafts(self, user_id: int, sport: str, season: int) -> list:
    """Fetch drafts for a user.

    Args:
      user_id: User id to request.
      sport: Sport key.
      season: Season year.

    Returns:
      Draft payloads.
    """
    return self.get_by_path(f"user/{user_id}/drafts/{sport}/{season}")

  def get_league(self, league_id: int) -> dict:
    """Fetch a league.

    Args:
      league_id: League id to request.

    Returns:
      League payload.
    """
    return self.get_by_path(f"league/{league_id}")

  def get_league_users(self, league_id: int) -> list:
    """Fetch league users.

    Args:
      league_id: League id to request.

    Returns:
      User payloads.
    """
    return self.get_by_path(f"league/{league_id}/users")

  def get_league_rosters(self, league_id: int) -> list:
    """Fetch league rosters.

    Args:
      league_id: League id to request.

    Returns:
      Roster payloads.
    """
    return self.get_by_path(f"league/{league_id}/rosters")

  def get_league_drafts(self, league_id: int) -> list:
    """Fetch league drafts.

    Args:
      league_id: League id to request.

    Returns:
      Draft payloads.
    """
    return self.get_by_path(f"league/{league_id}/drafts")

  def get_league_matchups(self, league_id: int, week: int) -> list:
    """Fetch league matchups for a week.

    Args:
      league_id: League id to request.
      week: Week number to request.

    Returns:
      Matchup payloads.
    """
    return self.get_by_path(f"league/{league_id}/matchups/{week}")

  def get_league_transactions(self, league_id: int, week: int) -> list:
    """Fetch league transactions for a week.

    Args:
      league_id: League id to request.
      week: Week number to request.

    Returns:
      Transaction payloads.
    """
    return self.get_by_path(f"league/{league_id}/transactions/{week}")

  def get_draft(self, draft_id: int) -> dict:
    """Fetch a draft.

    Args:
      draft_id: Draft id to request.

    Returns:
      Draft payload.
    """
    return self.get_by_path(f"draft/{draft_id}")

  def get_draft_picks(self, draft_id: int) -> list:
    """Fetch draft picks.

    Args:
      draft_id: Draft id to request.

    Returns:
      Pick payloads.
    """
    return self.get_by_path(f"draft/{draft_id}/picks")

  def get_draft_traded_picks(self, draft_id: int) -> list:
    """Fetch traded draft picks.

    Args:
      draft_id: Draft id to request.

    Returns:
      Traded pick payloads.
    """
    return self.get_by_path(f"draft/{draft_id}/traded_picks")

  def get_sport_state(self, sport: str) -> dict:
    """Fetch state for a sport.

    Args:
      sport: Sport key.

    Returns:
      Sport state payload.
    """
    return self.get_by_path(f"state/{sport}")

  def get_players(self, sport: str, season: str) -> dict:
    """Fetch player data for a sport and season.

    Args:
      sport: Sport key.
      season: Season year.

    Returns:
      Player payload.
    """
#    return self.get_by_path(f"players/{sport}")
    return self.get_by_root_path(f"projections/{sport}/{season}?season_type=regular")

  def get_stats(self, sport: str, season_type: str, season: int) -> dict:
    """Fetch season stats.

    Args:
      sport: Sport key.
      season_type: Season type.
      season: Season year.

    Returns:
      Stats payload.
    """
    return self.get_by_path(f"stats/{sport}/{season_type}/{season}")

  def get_week_stats(self, sport: str, season_type: str, season: int, week: int) -> dict:
    """Fetch weekly stats.

    Args:
      sport: Sport key.
      season_type: Season type.
      season: Season year.
      week: Week number.

    Returns:
      Stats payload.
    """
    return self.get_by_path(f"stats/{sport}/{season_type}/{season}/{week}")

  def get_projections(self, sport: str, season_type: str, season: int) -> dict:
    """Fetch season projections.

    Args:
      sport: Sport key.
      season_type: Season type.
      season: Season year.

    Returns:
      Projection payload.
    """
    return self.get_by_path(f"projections/{sport}/{season_type}/{season}")

  def get_week_projections(self, sport: str, season_type: str, season: int, week: int) -> dict:
    """Fetch weekly projections.

    Args:
      sport: Sport key.
      season_type: Season type.
      season: Season year.
      week: Week number.

    Returns:
      Projection payload.
    """
    return self.get_by_path(f"projections/{sport}/{season_type}/{season}/{week}")
