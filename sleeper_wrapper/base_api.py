from __future__ import annotations

from .api_client import SleeperApiClient


class BaseApi:
  _client: SleeperApiClient | None = None

  @classmethod
  def get_client(cls) -> SleeperApiClient:
    if cls._client is None:
      cls._client = SleeperApiClient()
    return cls._client

  @classmethod
  def set_client(cls, client: SleeperApiClient) -> None:
    cls._client = client
