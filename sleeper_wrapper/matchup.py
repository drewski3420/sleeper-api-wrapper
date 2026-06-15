"""Matchup models and sorting helpers."""

POSITION_ORDER = {
  "QB": 0,
  "RB": 1,
  "WR": 2,
  "TE": 3,
  "FLEX": 4,
  "SUPERFLEX": 5,
}

FLEX_POSITIONS = {"WR", "RB", "TE"}
SUPERFLEX_POSITIONS = {"WR", "RB", "TE", "QB"}


def get_position_sort_key(player) -> tuple[int, str]:
  """Build a sort key for matchup players.

  Args:
    player: Matchup player-like object with player_obj.

  Returns:
    Tuple used for position sorting.
  """
  player_obj = getattr(player, "player_obj", None)
  position = getattr(player_obj, "position", None)

  if position == "QB":
    return (POSITION_ORDER["QB"], position)
  if position == "RB":
    return (POSITION_ORDER["RB"], position)
  if position == "WR":
    return (POSITION_ORDER["WR"], position)
  if position == "TE":
    return (POSITION_ORDER["TE"], position)
  if position in FLEX_POSITIONS:
    return (POSITION_ORDER["FLEX"], position)
  if position in SUPERFLEX_POSITIONS:
    return (POSITION_ORDER["SUPERFLEX"], position)

  return (999, position or "")


class MatchupPlayer:
  """Represent a player entry in a matchup."""

  def __init__(self, player_id: str, points: float, starters: list[str]):
    """Initialize a matchup player.

    Args:
      player_id: Player id for the entry.
      points: Fantasy points scored.
      starters: Starter player ids for the roster.
    """
    self.player_id = player_id
    self.points = points
    self.is_starter = 1 if player_id in starters else 0
    self.is_bench = 1 if player_id not in starters else 0
    self.player_obj = None

  def __str__(self):
    """Return a readable player snapshot."""
    return str(self.__dict__)


class MatchupTeam:
  """Represent one roster in a matchup."""

  def __init__(self, data: dict):
    """Initialize a matchup team.

    Args:
      data: Raw matchup team payload.
    """
    self._data = data
    self.roster_id = int(self._data["roster_id"])
    self.points = self._data["points"]
    self.players_with_points = self._get_player_points()
    self.starter_points = sum(player.points for player in self.players_with_points if player.is_starter == 1)
    self.bench_points = sum(player.points for player in self.players_with_points if player.is_bench == 1)
    self.matchup_id = self._data["matchup_id"]
    self.team_obj = None

  def _get_player_points(self) -> list[MatchupPlayer]:
    """Build matchup players from points data.

    Returns:
      Matchup players for the roster.
    """
    players_points = self._data.get("players_points") or {}
    starters = self._data.get("starters") or []
    players = []

    for player_id, points in players_points.items():
      players.append(MatchupPlayer(player_id=player_id, points=points, starters=starters))

    players.sort(key=get_position_sort_key)
    return players

  def sort_players_by_position(self) -> None:
    """Sort matchup players by position."""
    self.players_with_points.sort(key=get_position_sort_key)

  def __str__(self):
    """Return a readable team snapshot."""
    return str(self.__dict__)


class Matchup:
  """Represent a full matchup."""

  def __init__(self, matchup_id: int, data: list[dict]):
    """Initialize a matchup.

    Args:
      matchup_id: Matchup id to assign.
      data: Raw matchup team payloads.
    """
    self._data = data
    self.matchup_id = int(matchup_id)
    self.teams = [MatchupTeam(e) for e in data]
    self.winning_roster_id = None
    self.losing_roster_id = None
    self.winning_team = None
    self.losing_team = None
    self._determine_outcome()
    self.teams = [self.winning_team, self.losing_team]

  def _determine_outcome(self) -> None:
    """Determine winner and loser for the matchup."""
    if len(self.teams) < 2:
      if len(self.teams) == 1:
        self.winning_roster_id = self.teams[0].roster_id
        self.winning_team = self.teams[0]
      return

    t1 = self.teams[0]
    t2 = self.teams[1]
    if t1.points > t2.points:
      self.winning_roster_id = t1.roster_id
      self.losing_roster_id = t2.roster_id
      self.winning_team = t1
      self.losing_team = t2
    else:
      self.winning_roster_id = t2.roster_id
      self.losing_roster_id = t1.roster_id
      self.winning_team = t2
      self.losing_team = t1

  def __str__(self):
    """Return a readable matchup summary."""
    if self.winning_team is None:
      return f"Matchup Number: {self.matchup_id}"

    if self.losing_team is None:
      winner_name = self.winning_team.team_obj.team_name if self.winning_team.team_obj else self.winning_team.roster_id
      return f"Matchup Number: {self.matchup_id} - {winner_name} ({self.winning_team.points})"

    return (
      f"Matchup Number: {self.matchup_id} - "
      + (
        " def. ".join(
          [
            f"{t.team_obj.team_name if t.team_obj else t.roster_id} ({t.points})"
            for t in self.teams
          ]
        )
      )
    )
