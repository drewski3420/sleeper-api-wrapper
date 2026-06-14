from __future__ import annotations

from typing import Any

import requests


class SleeperApiClient:
  def __init__(self, base_url: str = "https://api.sleeper.app/v1") -> None:
    self.base_url = base_url.rstrip("/")

  def get(self, url: str) -> Any:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

  def get_by_path(self, path: str) -> Any:
    normalized_path = path.lstrip("/")
    return self.get(f"{self.base_url}/{normalized_path}")

  def get_user(self, user_input: int) -> dict:
    return self.get_by_path(f"user/{user_input}")

  def get_user_leagues(self, user_id: int, sport: str, season: int) -> list:
    return self.get_by_path(f"user/{user_id}/leagues/{sport}/{season}")

  def get_user_drafts(self, user_id: int, sport: str, season: int) -> list:
    return self.get_by_path(f"user/{user_id}/drafts/{sport}/{season}")

  def get_league(self, league_id: int) -> dict:
    return self.get_by_path(f"league/{league_id}")

  def get_league_users(self, league_id: int) -> list:
    return self.get_by_path(f"league/{league_id}/users")

  def get_league_rosters(self, league_id: int) -> list:
    return self.get_by_path(f"league/{league_id}/rosters")

  def get_league_drafts(self, league_id: int) -> list:
    return self.get_by_path(f"league/{league_id}/drafts")

  def get_league_matchups(self, league_id: int, week: int) -> list:
    return self.get_by_path(f"league/{league_id}/matchups/{week}")

  def get_league_transactions(self, league_id: int, week: int) -> list:
    return self.get_by_path(f"league/{league_id}/transactions/{week}")

  def get_draft(self, draft_id: int) -> dict:
    return self.get_by_path(f"draft/{draft_id}")

  def get_draft_picks(self, draft_id: int) -> list:
    return self.get_by_path(f"draft/{draft_id}/picks")

  def get_draft_traded_picks(self, draft_id: int) -> list:
    return self.get_by_path(f"draft/{draft_id}/traded_picks")

  def get_sport_state(self, sport: str) -> dict:
    return self.get_by_path(f"state/{sport}")

  def get_players(self, sport: str) -> dict:
    return self.get_by_path(f"players/{sport}")

  def get_stats(self, sport: str, season_type: str, season: int) -> dict:
    return self.get_by_path(f"stats/{sport}/{season_type}/{season}")

  def get_week_stats(self, sport: str, season_type: str, season: int, week: int) -> dict:
    return self.get_by_path(f"stats/{sport}/{season_type}/{season}/{week}")

  def get_projections(self, sport: str, season_type: str, season: int) -> dict:
    return self.get_by_path(f"projections/{sport}/{season_type}/{season}")

  def get_week_projections(self, sport: str, season_type: str, season: int, week: int) -> dict:
    return self.get_by_path(f"projections/{sport}/{season_type}/{season}/{week}")
