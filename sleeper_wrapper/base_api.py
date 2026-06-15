"""Shared API client access for wrapper objects."""

from __future__ import annotations

from .api_client import SleeperApiClient


class BaseApi:
  """Base class that manages a shared API client."""

  _client: SleeperApiClient | None = None

  @classmethod
  def get_client(cls) -> SleeperApiClient:
    """Return the shared API client.

    Returns:
      Shared Sleeper API client.
    """
    if cls._client is None:
      cls._client = SleeperApiClient()
    return cls._client

  @classmethod
  def set_client(cls, client: SleeperApiClient) -> None:
    """Set the shared API client.

    Args:
      client: Client instance to use.
    """
    cls._client = client
