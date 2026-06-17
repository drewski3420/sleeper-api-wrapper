# models/matchup.py
"""Matchup models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .team import Team
  from .player import Player


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


@dataclass
class MatchupPlayer:
  player_id: str
  points: float
  starters: list[str]
  is_starter: int = field(init=False)
  is_bench: int = field(init=False)
  player_obj: "Player | None" = None

  def __post_init__(self) -> None:
    self.is_starter = 1 if self.player_id in self.starters else 0
    self.is_bench = 1 if self.player_id not in self.starters else 0


@dataclass
class MatchupTeam:
  roster_id: int
  points: float
  matchup_id: int
  players_with_points: list[MatchupPlayer] = field(default_factory=list)
  team_obj: "Team | None" = None
  starter_points: float = 0
  bench_points: float = 0

  @classmethod
  def from_payload(cls, data: dict) -> "MatchupTeam":
    players_points = data.get("players_points") or {}
    starters = data.get("starters") or []
    players = [
      MatchupPlayer(player_id=player_id, points=points, starters=starters)
      for player_id, points in players_points.items()
    ]
    players.sort(key=get_position_sort_key)

    team = cls(
      roster_id=int(data["roster_id"]),
      points=data["points"],
      matchup_id=data["matchup_id"],
      players_with_points=players,
    )
    team.starter_points = sum(p.points for p in players if p.is_starter == 1)
    team.bench_points = sum(p.points for p in players if p.is_bench == 1)
    return team

#  @classmethod
#  def sort_players_by_position(self) -> None:
#    self.players_with_points.sort(key=get_position_sort_key)

@dataclass
class Matchup:
  matchup_id: int
  teams: list[MatchupTeam] = field(default_factory=list)
  winning_roster_id: int | None = None
  losing_roster_id: int | None = None
  winning_team: MatchupTeam | None = None
  losing_team: MatchupTeam | None = None

  @classmethod
  def from_payload(cls, matchup_id: int, data: list[dict]) -> "Matchup":
    matchup = cls(matchup_id=int(matchup_id), teams=[MatchupTeam.from_payload(e) for e in data])
    matchup._determine_outcome()
    return matchup

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
