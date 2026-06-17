"""Shared API client access for wrapper objects."""

from __future__ import annotations

from .api_client import SleeperApiClient

class BaseApi:
  def __init__(self, client: SleeperApiClient | None = None):
    self.client = client or SleeperApiClient()
