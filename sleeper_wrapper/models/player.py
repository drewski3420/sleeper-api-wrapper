"""Player model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Player:
  """Represent a Sleeper player."""

  player_id: str
  player_data: dict | None = None
  _data: dict = field(init=False, repr=False)
  first_name: str | None = field(init=False)
  last_name: str | None = field(init=False)
  full_name: str = field(init=False)
  position: str | None = field(init=False)
  stats: dict = field(init=False)

  def __post_init__(self) -> None:
    """Initialize derived player fields."""
    self.player_id = str(self.player_id)
    self._data = self.player_data or {}

    self.first_name = self._data.get("first_name")
    self.last_name = self._data.get("last_name")
    self.full_name = self._get_full_name()
    self.position = self._data.get("position")
    self.stats = self._data.get("stats") or {}

  def __str__(self) -> str:
    """Return a readable player summary."""
    if self.position:
      return f"{self.position} {self.full_name}"
    return self.full_name

  def _get_full_name(self) -> str:
    """Build the player full name.

    Returns:
      Player full name or fallback id.
    """
    full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
    return full_name or self.player_id
