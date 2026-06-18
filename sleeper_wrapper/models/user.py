"""User model."""

from __future__ import annotations


class User:
  def __init__(self, user_name: int, user_data: dict | None = None) -> None:
    self._data = user_data or {}
    self.user_id = int(self._data.get("user_id"))
    self.username = self._data.get("username", user_name)
    self.display_name = self._data.get("display_name")
    self.metadata = self._data.get("metadata") or {}

  def __str__(self):
    return f"User: {self.username} User ID: {self.user_id} Display Name: {self.display_name}"
