"""Transaction models."""

from datetime import datetime

class TransactionPlayer:
  """Represent a player moved in a transaction."""

  def __init__(self, player_id: int):
    """Initialize a transaction player.

    Args:
      player_id: Player id involved in the transaction.
    """
    self.player_id = player_id
    self.player_obj = None

class TransactionPick:
  """Represent a draft pick moved in a transaction."""

  def __init__(self, data: dict):
    """Initialize a transaction pick.

    Args:
      data: Raw draft pick transaction payload.
    """
    self._data = data
    self.round_number = self._data['round']
    self.season = int(self._data['season'])
    self.old_roster_id = int(self._data['previous_owner_id'])
    self.new_roster_id = int(self._data['owner_id'])

class TransactionTeam:
  """Represent one team in a transaction."""

  def __init__(
      self,
      team_num: str,
      roster_id: int
  ):
    """Initialize a transaction team.

    Args:
      team_num: Label for the team in the transaction.
      roster_id: Roster id for the team.
    """
    self.team_num = team_num
    self.roster_id = int(roster_id)

    # populate later
    self.team_obj = None
    self.user_obj = None
    self.players_added = []
    self.players_dropped = []
    self.picks_added = []
    self.picks_lost = []

#  def __str__(self):
#    return f"{self.team_num}: {self.roster_id}"

class Transaction:
  """Represent a generic league transaction."""

  def __init__(self, data: dict):
    """Initialize a transaction.

    Args:
      data: Raw transaction payload.
    """
    self._data = data
    self.transaction_id = int(data.get("transaction_id"))
    self.transaction_type = data.get("type")
    self.status = data.get("status")

    status_updated = data.get("status_updated")
    created = data.get("created")
    self.status_updated = datetime.fromtimestamp(status_updated / 1000) if status_updated is not None else None
    self.creator = data.get("creator")
    self.created = datetime.fromtimestamp(created / 1000) if created is not None else None

    self.teams = [
      TransactionTeam(
        team_num=f"team{i}",
        roster_id=roster_id
      )
      for i, roster_id in enumerate(
          data.get("roster_ids", []),
          start=1
      )
    ]
    self.teams_by_roster_id = {team.roster_id: team for team in self.teams}

    self.adds = {player_id: int(roster_id) for player_id, roster_id in (data.get("adds") or {}).items()}
    self.drops = {player_id: int(roster_id) for player_id, roster_id in (data.get("drops") or {}).items()}
    self._populate_adds()
    self._populate_drops()
    self._populate_picks()

  def _populate_picks(self) -> None:
    """Attach moved picks to transaction teams."""
    for p in self._data.get('draft_picks', []):
      pick = TransactionPick(p)

      if pick.new_roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[pick.new_roster_id].picks_added.append(pick)

      if pick.old_roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[pick.old_roster_id].picks_lost.append(pick)

  def _populate_drops(self) -> None:
    """Attach dropped players to transaction teams."""
    for player_id, roster_id in self.drops.items():
      if roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[roster_id].players_dropped.append(TransactionPlayer(player_id))

  def _populate_adds(self) -> None:
    """Attach added players to transaction teams."""
    for player_id, roster_id in self.adds.items():
      if roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[roster_id].players_added.append(TransactionPlayer(player_id))

#  def __repr__(self):
#    return (
#      f"{self.__class__.__name__}"
#      f"(id={self.transaction_id}, status={self.status},transaction_type={self.transaction_type})"
#    )

class Trade(Transaction):
  """Represent a trade transaction."""

  def __init__(self, data: dict):
    """Initialize a trade.

    Args:
      data: Raw transaction payload.
    """
    super().__init__(data)

    self.draft_picks = data.get("draft_picks", [])
    self.waiver_budget = data.get("waiver_budget", [])

    self.adds = {player_id: int(roster_id) for player_id, roster_id in (data.get("adds") or {}).items()}
    self.drops = {player_id: int(roster_id) for player_id, roster_id in (data.get("drops") or {}).items()}

#  def __str__(self):
#    return (
#      f"Trade("
#      f"rosters={self.roster_ids}, "
#      f"picks={len(self.draft_picks)}"
#      f")"
#    )

class FreeAgent(Transaction):
  """Represent a free agent transaction."""

  def __init__(self, data: dict):
    """Initialize a free agent transaction.

    Args:
      data: Raw transaction payload.
    """
    super().__init__(data)

#  #Free Agent has no additional properties
#  def __str__(self):
#    return (
#      f"FreeAgent("
#      f"adds={len(self.adds)}, "
#      f"drops={len(self.drops)}"
#      f")"
#    )


class Waiver(Transaction):
  """Represent a waiver transaction."""

  def __init__(self, data: dict):
    """Initialize a waiver transaction.

    Args:
      data: Raw transaction payload.
    """
    super().__init__(data)

    self.added_player_ids = list((self.adds or {}).keys())
    self.dropped_player_ids = list((self.drops or {}).keys())
    self.added_players = []
    self.dropped_players = []

    self.waiver_bid = (int(data.get("settings", {}).get("waiver_bid")) if data.get("settings") else None)
    self.waiver_seq = (int(data.get("settings", {}).get("seq")) if data.get("settings") else None)

    self.message = data.get('metadata',{}).get('notes')

#  def __str__(self):
#    return (
#      f"Waiver("
#      f"bid={self.waiver_bid}, "
#      f"adds={len(self.added_player_ids)}, "
#      f"drops={len(self.dropped_player_ids)}"
#      f")"
#    )
