"""User model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class User:
  user_name: int | str
  user_data: dict | None = None
  _data: dict = field(init=False, repr=False)
  user_id: int = field(init=False)
  username: int | str = field(init=False)
  display_name: str | None = field(init=False)
  metadata: dict = field(init=False)

  def __post_init__(self) -> None:
    self._data = self.user_data or {}
    self.user_id = int(self._data.get("user_id"))
    self.username = self._data.get("username", self.user_name)
    self.display_name = self._data.get("display_name")
    self.metadata = self._data.get("metadata") or {}

  def __str__(self) -> str:
    return f"User: {self.username} User ID: {self.user_id} Display Name: {self.display_name}"
