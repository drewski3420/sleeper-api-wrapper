"""Stats and projections helpers."""

import logging

from sleeper_wrapper.base_api import BaseApi

logger = logging.getLogger(__name__)

warning_message = "The Stats API is no longer included in Sleeper's documentation, therefore we cannot guarantee that this class will continue working."


class Stats(BaseApi):
  """Retrieve stats and projections from Sleeper."""

  def __init__(self, sport: str):
    """Initialize stats access.

    Args:
      sport: Sport key to query.
    """
    logger.warning(warning_message)
    self._sport = sport

  def get_all_stats(self, season_type: str, season: int) -> dict:
    """Retrieve season stats.

    Args:
      season_type: Season type to query.
      season: Season year to query.

    Returns:
      Stats keyed by player.
    """
    return self.get_client().get_stats(self._sport, season_type, season)

  def get_week_stats(self, season_type: str, season: int, week: int) -> dict:
    """Retrieve weekly stats.

    Args:
      season_type: Season type to query.
      season: Season year to query.
      week: Week number to query.

    Returns:
      Stats keyed by player.
    """
    return self.get_client().get_week_stats(self._sport, season_type, season, week)

  def get_all_projections(self, season_type: str, season: int) -> dict:
    """Retrieve season projections.

    Args:
      season_type: Season type to query.
      season: Season year to query.

    Returns:
      Projections keyed by player.
    """
    return self.get_client().get_projections(self._sport, season_type, season)

  def get_week_projections(self, season_type: str, season: int, week: int) -> dict:
    """Retrieve weekly projections.

    Args:
      season_type: Season type to query.
      season: Season year to query.
      week: Week number to query.

    Returns:
      Projections keyed by player.
    """
    return self.get_client().get_week_projections(self._sport, season_type, season, week)

  def get_player_week_stats(self, stats: dict, player_id: str) -> dict | None:
    """Get player stats from a stats dictionary.

    Args:
      stats: Stats or projections dictionary.
      player_id: Player id to look up.

    Returns:
      Player stats if present.
    """
    return stats.get(player_id, None)

  def get_player_week_score(self, stats: dict, player_id: str) -> dict | None:
    """Get primary fantasy scores for a player.

    Args:
      stats: Stats or projections dictionary.
      player_id: Player id to look up.

    Returns:
      Primary scoring values if present.
    """
    result_dict = {}
    player_stats = stats.get(player_id, None)

    if player_stats:
      result_dict["pts_ppr"] = player_stats.get("pts_ppr", None)
      result_dict["pts_std"] = player_stats.get("pts_std", None)
      result_dict["pts_half_ppr"] = player_stats.get("pts_half_ppr", None)

    return result_dict
