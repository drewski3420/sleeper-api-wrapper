from typing import Union

from .base_api import BaseApi
from .player import Player

class Pick:
  """The data associated with a pick in a Sleep draft.

  Attributes:
    overall_pick: int
      Overall pick number
    round_number: int
      Pick's round number
    round_pick_number: int
      Pick Number within round
    roster_id: int
      Roster ID of picking team
    team_name: str
      Team Name of picking team
    user_id: int
      User ID of picking team
    player_id: int
      Sleeper ID of player
#    metadata: Player
#      Raw metadata of Player object
  """
  def __init__(self, data):
    """Initializes the Pick based on JSON data.

    Args:
      data: Dict
          The raw data of the pick from Drafts class.
    """
    self.__dict__.update(data) #expand all properties
#    self.overall_pick = data.get("pick_no")
#    self.round_pick_number = self._get_round_pick_number(self.overall_pick)
#    self.round_number = data.get("round")
#    self.roster_id = data.get("roster_id")
##    self.team_name = self._get_team_name(self.roster_id)
##    self.user_id = self._get_user_id(self.roster_id)
#    self.player_id = data.get("player_id")
#    self.draft_id = data.get("draft_id")
    self.player = self._get_player()
    self.raw = data

  def _get_player(self) -> Player:
    return Player(self.metadata['player_id'], self.metadata)
    #Player(player_info)

  def _get_round_pick_number(self, overall_pick: int) -> int:
    return ((overall_pick - 1) % 8) + 1

#  def _get_team_name(self, roster_id: int) -> str:
#    user_id = self.roster_id_to_user_id.get(int(roster_id))
#    if user_id is None:
#        return None
#    return self.user_id_to_team_name.get(user_id)
#roster_id_to_user_id = l.map_rosterid_to_ownerid(l.get_rosters())
#  user_id_to_team_name = l.map_users_to_team_name(l.get_users())


#  def get_specific_draft(self) -> dict:
#    """Returns the draft's data."""
#    return self._call(self._base_url)
#
#  def get_all_picks(self) -> list:
#    """Returns all the picks in the specified draft."""
#    return self._call("{}/{}".format(self._base_url,"picks"))
#
#  def get_traded_picks(self) -> list:
#    """Returns all the traded picks in the specified draft."""
#    return self._call("{}/{}".format(self._base_url,"traded_picks"))
