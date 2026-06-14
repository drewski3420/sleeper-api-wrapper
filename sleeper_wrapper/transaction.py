from typing import Union
from datetime import datetime
from .base_api import BaseApi
from .player import Player
from .user import User

from .player import Player


"""
'created': 1757458201289, 
'settings': {'seq': 4, 'waiver_bid': 0}, 
'leg': 1, 
'draft_picks': [], 
'creator': '606232341194534912', 
'transaction_id': '1271275473288040448', 
'adds': {'12472': 5}, 
'drops': None, 
'consenter_ids': [5], 
'roster_ids': [5], 
'status_updated': 1757577658636, 
'waiver_budget': []
"""
class Transaction:
  def __init__(self, data: dict):
    self._data = data
    self.transaction_id = int(data.get("transaction_id"))
    self.transaction_type = data.get("type")
    self.status = data.get("status")
    self.status_updated = datetime.fromtimestamp(data.get("status_updated")/1000)

    self.creator = data.get("creator")
    self.created = datetime.fromtimestamp(data.get("created")/1000)

    self.roster_ids = data.get("roster_ids", [])

    self.settings = data.get("settings")
#    self.adds = data.get("adds") or {}
#    self.drops = data.get("drops") or {}

  def __repr__(self):
    return (
      f"{self.__class__.__name__}"
      f"(id={self.transaction_id}, status={self.status},transaction_type={self.transaction_type})"
    )


class Trade(Transaction):
  def __init__(self, data: dict):
    super().__init__(data)

    self.draft_picks = data.get("draft_picks", [])
    self.waiver_budget = data.get("waiver_budget", [])

    self.adds = data.get("adds") or {}
    self.drops = data.get("drops") or {}

  def __str__(self):
    return (
      f"Trade("
      f"rosters={self.roster_ids}, "
      f"picks={len(self.draft_picks)}"
      f")"
    )

class FreeAgent(Transaction):
  def __init__(self, data: dict):
    super().__init__(data)

#    self.adds = data.get("adds") or {}
    self.drops = data.get("drops") or {}
    self.message = "Free Agent"
  def __str__(self):
    return (
      f"FreeAgent("
      f"adds={len(self.adds)}, "
      f"drops={len(self.drops)}"
      f")"
    )


class Waiver(Transaction):
  def __init__(self, data: dict):
    super().__init__(data)

    self.added_player_ids = data.get("adds").keys() or []
    self.dropped_player_ids = data.get("drops").keys() or []
    self.added_players = []
    self.dropped_players = []

    self.waiver_bid = (int(data.get("settings", {}).get("waiver_bid")) if data.get("settings") else 0)

  def __str__(self):
    return (
      f"Waiver("
      f"bid={self.waiver_bid}, "
      f"adds={len(self.adds)}, "
      f"drops={len(self.drops)}"
      f")"
    )
