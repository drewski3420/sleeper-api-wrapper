from sleeper_wrapper.all_players import AllPlayers
from sleeper_wrapper.base_api import BaseApi
from sleeper_wrapper.draft import Draft
from sleeper_wrapper.league import League
from sleeper_wrapper.matchup import Matchup
from sleeper_wrapper.transaction import Transaction
from sleeper_wrapper.user import User


class FakeClient:
  def get_league(self, league_id: int) -> dict:
    return {
      "league_id": league_id,
      "season": "2024",
      "sport": "nfl",
      "settings": {
        "start_week": 1,
        "last_scored_leg": 2,
        "playoff_week_start": 15,
      },
      "scoring_settings": {},
      "total_rosters": 2,
      "status": "in_season",
      "name": "Test League",
    }

  def get_league_users(self, league_id: int) -> list:
    return [
      {
        "user_id": "101",
        "username": "alpha",
        "display_name": "Alpha",
        "metadata": {"team_name": "Alpha Team"},
      },
      {
        "user_id": "102",
        "username": "beta",
        "display_name": "Beta",
        "metadata": {"team_name": "Beta Team"},
      },
    ]

  def get_league_rosters(self, league_id: int) -> list:
    return [
      {"roster_id": "1", "owner_id": "101"},
      {"roster_id": "2", "owner_id": "102"},
    ]

  def get_league_drafts(self, league_id: int) -> list:
    return [{"draft_id": "5001"}]

  def get_sport_state(self, sport: str) -> dict:
    return {"league_season": "2024"}

  def get_draft(self, draft_id: int) -> dict:
    return {
      "draft_id": draft_id,
      "last_picked": 1700000000000,
      "start_time": 1699990000000,
      "type": "snake",
      "metadata": {"scoring_type": "ppr"},
    }

  def get_draft_picks(self, draft_id: int) -> list:
    return [
      {
        "pick_no": 1,
        "round": 1,
        "picked_by": "101",
        "metadata": {"player_id": "9001", "first_name": "Josh", "last_name": "Allen", "position": "QB"},
      }
    ]

  def get_draft_traded_picks(self, draft_id: int) -> list:
    return []

  def get_players(self, sport: str) -> dict:
    return {
      "9001": {"first_name": "Josh", "last_name": "Allen", "position": "QB", "stats": {"adp_std": 1.0}},
      "12472": {"first_name": "Bijan", "last_name": "Robinson", "position": "RB", "stats": {"adp_std": 2.0}},
      "22222": {"first_name": "CeeDee", "last_name": "Lamb", "position": "WR", "stats": {"adp_std": 3.0}},
    }

  def get_league_matchups(self, league_id: int, week: int) -> list:
    return [
      {
        "roster_id": "1",
        "points": 100.5,
        "matchup_id": 1,
        "starters": ["9001"],
        "players_points": {"9001": 25.0},
      },
      {
        "roster_id": "2",
        "points": 95.0,
        "matchup_id": 1,
        "starters": ["22222"],
        "players_points": {"22222": 20.0},
      },
    ]

  def get_league_transactions(self, league_id: int, week: int) -> list:
    return [
      {
        "transaction_id": "7001",
        "type": "waiver",
        "status": "complete",
        "status_updated": 1700000000000,
        "creator": "101",
        "created": 1699990000000,
        "roster_ids": ["1"],
        "adds": {"12472": "1"},
        "drops": {"22222": "1"},
        "settings": {"waiver_bid": 10, "seq": 1},
        "metadata": {"notes": "Claim processed"},
        "draft_picks": [],
      }
    ]


class FakeClientMissingSettings(FakeClient):
  def get_league(self, league_id: int) -> dict:
    return {
      "league_id": league_id,
      "season": "2024",
      "sport": "nfl",
      "scoring_settings": {},
      "total_rosters": 2,
      "status": "in_season",
      "name": "No Settings League",
    }


def setup_function() -> None:
  BaseApi.set_client(FakeClient())
  AllPlayers._cache = {}


def test_league_normalizes_ids_and_builds_objects() -> None:
  league = League(123)

  assert league.league_id == 123
  assert isinstance(league.users[0], User)
  assert league.users[0].user_id == 101
  assert league.teams[0].roster_id == 1
  assert league.teams[0].user is league.users_by_id[101]
  assert league.drafts[0].draft_id == 5001


def test_pick_links_user_and_optional_team() -> None:
  league = League(123)

  draft = league.drafts[0]
  pick = draft.picks[0]

  assert isinstance(draft, Draft)
  assert pick.picked_by_user_id == 101
  assert pick.user is league.users_by_id[101]
  assert pick.team is league.teams_by_user_id[101]
  assert pick.team_name == "Alpha Team"


def test_transaction_enrichment_attaches_team_user_and_players() -> None:
  league = League(123)

  waivers = league.get_waivers(1)
  waiver = waivers[0]
  transaction_team = waiver.teams[0]

  assert transaction_team.team is league.teams_by_roster_id[1]
  assert transaction_team.user is league.users_by_id[101]
  assert transaction_team.players_added[0].player.full_name == "Bijan Robinson"
  assert transaction_team.players_dropped[0].player.full_name == "CeeDee Lamb"


def test_all_players_cache_is_keyed_by_sport_and_season() -> None:
  BaseApi.set_client(FakeClient())
  AllPlayers._cache = {}

  nfl_2024 = AllPlayers(2024, "nfl")
  nfl_2025 = AllPlayers(2025, "nfl")

  assert ("nfl", 2024) in AllPlayers._cache
  assert ("nfl", 2025) in AllPlayers._cache
  assert nfl_2024.players_by_id == nfl_2025.players_by_id


def test_league_handles_missing_settings() -> None:
  BaseApi.set_client(FakeClientMissingSettings())
  AllPlayers._cache = {}

  league = League(456)

  assert league.first_week is None
  assert league.most_recent_week is None
  assert league.get_results() == {}


def test_matchup_handles_single_team() -> None:
  matchup = Matchup(
    matchup_id=1,
    data=[
      {
        "roster_id": "1",
        "points": 100.5,
        "matchup_id": 1,
        "starters": ["9001"],
        "players_points": {"9001": 25.0},
      }
    ],
  )

  assert matchup.winning_roster_id == 1
  assert matchup.losing_roster_id is None
  assert matchup.losing_team is None


def test_transaction_handles_missing_timestamps_and_unknown_rosters() -> None:
  transaction = Transaction(
    {
      "transaction_id": "7002",
      "type": "trade",
      "status": "complete",
      "creator": "101",
      "roster_ids": ["1"],
      "adds": {"12472": "99"},
      "drops": {"22222": "99"},
      "draft_picks": [
        {
          "round": 1,
          "season": "2025",
          "previous_owner_id": "99",
          "owner_id": "1",
        }
      ],
    }
  )

  assert transaction.status_updated is None
  assert transaction.created is None
  assert len(transaction.teams[0].players_added) == 0
  assert len(transaction.teams[0].players_dropped) == 0
  assert len(transaction.teams[0].picks_added) == 1
  assert len(transaction.teams[0].picks_lost) == 0
