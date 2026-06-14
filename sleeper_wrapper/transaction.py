from datetime import datetime


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
class TransactionPlayer:
  def __init__(self, player_id: int):
    self.player_id = player_id
    self.player = None

class TransactionPick:
  def __init__(self, data: dict):
    self._data = data
    self.round_number = self._data['round']
    self.season = int(self._data['season'])
    self.old_roster_id = int(self._data['previous_owner_id'])
    self.new_roster_id = int(self._data['owner_id'])

class TransactionTeam:
  def __init__(
      self,
      team_num: str,
      roster_id: int
  ):
    self.team_num = team_num
    self.roster_id = roster_id

    # populate later
    self.team = None
    self.user = None
    self.players_added = []
    self.players_dropped = []
    self.picks_added = []
    self.picks_lost = []

#  def __str__(self):
#    return f"{self.team_num}: {self.roster_id}"

class Transaction:
  def __init__(self, data: dict):
    self._data = data
    self.transaction_id = int(data.get("transaction_id"))
    self.transaction_type = data.get("type")
    self.status = data.get("status")
    self.status_updated = datetime.fromtimestamp(data.get("status_updated")/1000)

    self.creator = data.get("creator")
    self.created = datetime.fromtimestamp(data.get("created")/1000)

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

    self.adds = data.get("adds") or {}
    self.drops = data.get("drops") or {}
    self._populate_adds()
    self._populate_drops()
    self._populate_picks()

  def _populate_picks(self) -> None:
    for p in self._data.get('draft_picks',[]):
      pick = TransactionPick(p)
      self.teams_by_roster_id[pick.new_roster_id].picks_added.append(pick)
      self.teams_by_roster_id[pick.old_roster_id].picks_lost.append(pick)

  def _populate_drops(self) -> None:
    for player_id, roster_id in self.drops.items():
      self.teams_by_roster_id[roster_id].players_dropped.append(TransactionPlayer(player_id))

  def _populate_adds(self) -> None:
    for player_id, roster_id in self.adds.items():
      self.teams_by_roster_id[roster_id].players_added.append(TransactionPlayer(player_id))

#  def __repr__(self):
#    return (
#      f"{self.__class__.__name__}"
#      f"(id={self.transaction_id}, status={self.status},transaction_type={self.transaction_type})"
#    )

class Trade(Transaction):
  def __init__(self, data: dict):
    super().__init__(data)

    self.draft_picks = data.get("draft_picks", [])
    self.waiver_budget = data.get("waiver_budget", [])

    self.adds = data.get("adds") or {}
    self.drops = data.get("drops") or {}

#  def __str__(self):
#    return (
#      f"Trade("
#      f"rosters={self.roster_ids}, "
#      f"picks={len(self.draft_picks)}"
#      f")"
#    )

class FreeAgent(Transaction):
  def __init__(self, data: dict):
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
  def __init__(self, data: dict):
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
