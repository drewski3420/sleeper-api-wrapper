"""Player model."""

class Player:
  """Represent a Sleeper player."""

  def __init__(
      self,
      player_id: str,
      player_data: dict | None = None,
  ):
      """Initialize a player.

      Args:
        player_id: Player id to assign.
        player_data: Raw player payload.
      """
      self.player_id = str(player_id)
      self._player_data = player_data or {}

      self.first_name = self._player_data.get('first_name')
      self.last_name = self._player_data.get('last_name')
      self.full_name = self._get_full_name()
      self.position = self._player_data.get('position')
      self.stats = self._player_data.get('stats')

  def __str__(self):
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
