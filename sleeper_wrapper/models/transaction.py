"""Transaction models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TransactionPlayer:
  """Represent a player moved in a transaction."""

  player_id: str
  player_obj: object | None = None


@dataclass
class TransactionPick:
  """Represent a draft pick moved in a transaction."""

  round_number: int
  season: int
  old_roster_id: int
  new_roster_id: int

  @classmethod
  def from_payload(cls, data: dict) -> "TransactionPick":
    return cls(
      round_number=int(data["round"]),
      season=int(data["season"]),
      old_roster_id=int(data["previous_owner_id"]),
      new_roster_id=int(data["owner_id"]),
    )


@dataclass
class TransactionTeam:
  """Represent one team in a transaction."""

  team_num: str
  roster_id: int
  team_obj: object | None = None
  user_obj: object | None = None
  players_added: list[TransactionPlayer] = field(default_factory=list)
  players_dropped: list[TransactionPlayer] = field(default_factory=list)
  picks_added: list[TransactionPick] = field(default_factory=list)
  picks_lost: list[TransactionPick] = field(default_factory=list)



@dataclass
class Transaction:
  """Represent a generic league transaction."""

  transaction_id: int
  transaction_type: str | None
  status: str | None
  status_updated: datetime | None
  creator: str | None
  created: datetime | None
  teams: list[TransactionTeam] = field(default_factory=list)
  teams_by_roster_id: dict[int, TransactionTeam] = field(default_factory=dict)
  adds: dict[str, int] = field(default_factory=dict)
  drops: dict[str, int] = field(default_factory=dict)
  _data: dict = field(default_factory=dict, repr=False)

  @classmethod
  def from_payload(cls, data: dict) -> "Transaction":
    transaction_id = int(data.get("transaction_id"))
    status_updated = data.get("status_updated")
    created = data.get("created")

    teams = [
      TransactionTeam(team_num=f"team{i}", roster_id=int(roster_id))
      for i, roster_id in enumerate(data.get("roster_ids", []), start=1)
    ]
    teams_by_roster_id = {team.roster_id: team for team in teams}

    adds = {player_id: int(roster_id) for player_id, roster_id in (data.get("adds") or {}).items()}
    drops = {player_id: int(roster_id) for player_id, roster_id in (data.get("drops") or {}).items()}

    tx = cls(
      transaction_id=transaction_id,
      transaction_type=data.get("type"),
      status=data.get("status"),
      status_updated=datetime.fromtimestamp(status_updated / 1000) if status_updated is not None else None,
      creator=data.get("creator"),
      created=datetime.fromtimestamp(created / 1000) if created is not None else None,
      teams=teams,
      teams_by_roster_id=teams_by_roster_id,
      adds=adds,
      drops=drops,
      _data=data,
    )
    tx._populate_adds()
    tx._populate_drops()
    tx._populate_picks()
    return tx

  def _populate_picks(self) -> None:
    for p in self._data.get("draft_picks", []):
      pick = TransactionPick.from_payload(p)

      if pick.new_roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[pick.new_roster_id].picks_added.append(pick)

      if pick.old_roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[pick.old_roster_id].picks_lost.append(pick)

  def _populate_drops(self) -> None:
    for player_id, roster_id in self.drops.items():
      if roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[roster_id].players_dropped.append(TransactionPlayer(player_id))

  def _populate_adds(self) -> None:
    for player_id, roster_id in self.adds.items():
      if roster_id in self.teams_by_roster_id:
        self.teams_by_roster_id[roster_id].players_added.append(TransactionPlayer(player_id))


@dataclass
class Trade(Transaction):
  """Represent a trade transaction."""

  draft_picks: list[dict] = field(default_factory=list)
  waiver_budget: list | None = None

  @classmethod
  def from_payload(cls, data: dict) -> "Trade":
    tx = super().from_payload(data)
    tx.__class__ = cls
    tx.draft_picks = data.get("draft_picks", [])
    tx.waiver_budget = data.get("waiver_budget", [])
    return tx


@dataclass
class FreeAgent(Transaction):
  """Represent a free agent transaction."""

  @classmethod
  def from_payload(cls, data: dict) -> "FreeAgent":
    tx = super().from_payload(data)
    tx.__class__ = cls
    return tx


@dataclass
class Waiver(Transaction):
  """Represent a waiver transaction."""

  added_player_ids: list[str] = field(default_factory=list)
  dropped_player_ids: list[str] = field(default_factory=list)
  added_players: list[TransactionPlayer] = field(default_factory=list)
  dropped_players: list[TransactionPlayer] = field(default_factory=list)
  waiver_bid: int | None = None
  waiver_seq: int | None = None
  message: str | None = None

  @classmethod
  def from_payload(cls, data: dict) -> "Waiver":
    tx = super().from_payload(data)
    tx.__class__ = cls
    tx.added_player_ids = list((tx.adds or {}).keys())
    tx.dropped_player_ids = list((tx.drops or {}).keys())
    tx.waiver_bid = int(data.get("settings", {}).get("waiver_bid")) if data.get("settings") else None
    tx.waiver_seq = int(data.get("settings", {}).get("seq", 0)) if data.get("settings") else None
    tx.message = data.get("metadata", {}).get("notes")
    return tx
