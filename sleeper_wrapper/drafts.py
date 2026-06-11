from typing import Union

from .base_api import BaseApi
from .pick import Pick

class Draft(BaseApi):
  """The data associated with a given Sleeper draft.

  Attributes:
    draft_id: Union[str, int]
      The Sleeper ID for the draft. May be provided as a string or int.
  """


  def __init__(self, draft_id: Union[str, int]) -> None:
    """Initializes the instance based on draft ID.

    Args:
      draft_id: Union[str, int]
          The Sleeper ID for the draft. May be provided as a string or int.
    """
    self.draft_id = draft_id
    self._base_url = f"https://api.sleeper.app/v1/draft/{self.draft_id}"

    self._picks = None
    self._traded_picks = None
    self._data = None

  def get_all_picks(self) -> list[Pick]:
    if self._picks is None:
      picks = self._call(f"{self._base_url}/picks")
      self._picks = [Pick(p) for p in picks]

    return self._picks

  def get_draft(self) -> dict:
    if self._data is None:
      self._data = self._call(self._base_url)

    return self._data


  def get_traded_picks(self) -> list:
    if self._traded_picks is None:
      self._traded_picks = self._call(f"{self._base_url}/traded_picks")

    return self._traded_picks

  def get_draft_rosters(self) -> list[Roster]:
