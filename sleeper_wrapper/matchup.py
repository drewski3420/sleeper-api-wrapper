class MatchupPlayer:
  def __init__(self, player_id: str, points: float, starters: list[str]):
    self.player_id = player_id
    self.points = points
    self.is_starter = 1 if player_id in starters else 0
    self.is_bench = 1 if player_id not in starters else 0
    self.player = None

  def __str__(self):
    return str(self.__dict__)


class TeamEntry:
  def __init__(self, data: dict):
    self._data = data
    self.roster_id = int(self._data["roster_id"])
    self.points = self._data["points"]
    self.players_with_points = self._get_player_points()
    self.starter_points = sum(player.points for player in self.players_with_points if player.is_starter == 1)
    self.bench_points = sum(player.points for player in self.players_with_points if player.is_bench == 1)
    self.matchup_id = self._data["matchup_id"]
    self.team_obj = None

  def _get_player_points(self) -> list[MatchupPlayer]:
    players_points = self._data.get("players_points") or {}
    starters = self._data.get("starters") or []
    players = []

    for player_id, points in players_points.items():
      players.append(MatchupPlayer(player_id=player_id, points=points, starters=starters))

    return players

  def __str__(self):
    return str(self.__dict__)


class Matchup:
  def __init__(self, matchup_id: int, data: list[dict]):
    self._data = data
    self.matchup_id = int(matchup_id)
    self.teams = [TeamEntry(e) for e in data]
    self.winning_roster_id = None
    self.losing_roster_id = None
    self.winning_team = None
    self.losing_team = None
    self._determine_outcome()

  def _determine_outcome(self) -> None:
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
            for t in [self.winning_team, self.losing_team]
          ]
        )
      )
    )
