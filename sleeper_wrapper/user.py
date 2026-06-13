from typing import Union

from .base_api import BaseApi

class User(BaseApi):
  """The data associated with a given Sleeper user."""

  def __init__(self, initial_user_input: Union[str, int]) -> None:
    self._base_url = "https://api.sleeper.app/v1/user"
    self._data = self._get_data(initial_user_input)
    self.user_id = self._data.get('user_id')
    self.username = self._data.get('username')
    self.display_name = self._data.get('display_name')

  def __str__(self):
    return f"User: {self.username} User ID: {self.user_id} Display Name: {self.display_name}"

  def _get_data(self, initial_user_input: Union[str, int]) -> dict:
    return self._call("{}/{}".format(self._base_url, initial_user_input))

  def get_all_leagues(self, season: Union[str, int], sport: str = "nfl") -> List[League]:
    from .league import League
    leagues = self._call("{}/{}/{}/{}/{}".format(self._base_url, self.user_id, "leagues", sport, season))
    return [League(l.get('league_id')) for l in leagues]

  def get_all_drafts(self, season: Union[str, int], sport: str = "nfl") -> list:
    drafts = self._call("{}/{}/{}/{}/{}".format(self._base_url, self._user_id, "drafts", sport, season))
    return [Draft(d.get('draft_id')) for d in drafts]
