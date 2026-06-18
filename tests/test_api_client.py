import pytest
from unittest.mock import Mock, patch

from sleeper_wrapper.api_client import SleeperApiClient

from fixtures import TEST_LEAGUE_SCENARIO

LEAGUE_ID = TEST_LEAGUE_SCENARIO['league_id']
USER_ID = TEST_LEAGUE_SCENARIO['users'][0]['user_id']
DRAFT_ID = TEST_LEAGUE_SCENARIO['drafts'][0]['draft_id']
SPORT = TEST_LEAGUE_SCENARIO['sport']
YEAR = TEST_LEAGUE_SCENARIO['sport_state']['season']
WEEK = TEST_LEAGUE_SCENARIO['sport_state']['week']

@pytest.fixture
def client():
  return SleeperApiClient(base_url="https://api.sleeper.app/v1")

@pytest.fixture
def mock_get():
  with patch("sleeper_wrapper.api_client.requests.get") as m:
    yield m

def test_get_builds_full_url(client, mock_get):
  mock_get.return_value.json.return_value = {"ok": True}

  client.get(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}")

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}"
  )

def test_get_by_path(client, mock_get):
  mock_get.return_value.json.return_value = {"x": 1}

  client.get_by_path(f"league/{LEAGUE_ID}")

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}"
  )

def test_get_by_root_path(client, mock_get):
  mock_get.return_value.json.return_value = {"x": 1}

  client.get_by_root_path(f"state/{SPORT}")

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/state/{SPORT}"
  )

def test_get_user(client, mock_get):
  mock_get.return_value.json.return_value = {"user_id": USER_ID}

  result = client.get_user(USER_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/user/{USER_ID}"
  )
  assert result["user_id"] == USER_ID

def test_get_user_leagues(client, mock_get):
  mock_get.return_value.json.return_value = [{"league_id": LEAGUE_ID}]

  client.get_user_leagues(USER_ID, SPORT, YEAR)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/user/{USER_ID}/leagues/{SPORT}/{YEAR}"
  )

def test_get_user_drafts(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_user_drafts(USER_ID, SPORT, YEAR)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/user/{USER_ID}/drafts/{SPORT}/{YEAR}"
  )

def test_get_league(client, mock_get):
  mock_get.return_value.json.return_value = {"league_id": LEAGUE_ID}

  result = client.get_league(LEAGUE_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}"
  )
  assert result["league_id"] == LEAGUE_ID

def test_get_league_users(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_league_users(LEAGUE_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users"
  )

def test_get_league_rosters(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_league_rosters(LEAGUE_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters"
  )

def test_get_league_drafts(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_league_drafts(LEAGUE_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/drafts"
  )

def test_get_league_matchups(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_league_matchups(LEAGUE_ID, WEEK)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/{WEEK}"
  )

def test_get_league_transactions(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_league_transactions(LEAGUE_ID, WEEK)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/{WEEK}"
  )

def test_get_draft(client, mock_get):
  mock_get.return_value.json.return_value = {"draft_id": DRAFT_ID}

  client.get_draft(DRAFT_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/draft/{DRAFT_ID}"
  )

def test_get_draft_picks(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_draft_picks(DRAFT_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/draft/{DRAFT_ID}/picks"
  )

def test_get_draft_traded_picks(client, mock_get):
  mock_get.return_value.json.return_value = []

  client.get_draft_traded_picks(DRAFT_ID)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/draft/{DRAFT_ID}/traded_picks"
  )

def test_get_sport_state(client, mock_get):
  mock_get.return_value.json.return_value = {"week": WEEK}

  client.get_sport_state(SPORT)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/state/nfl"
  )

def test_get_players(client, mock_get):
  mock_get.return_value.json.return_value = {}

  client.get_players(SPORT, YEAR)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/projections/{SPORT}/{YEAR}?season_type=regular"
  )

def test_get_stats(client, mock_get):
  mock_get.return_value.json.return_value = {}

  client.get_stats(SPORT, "regular", YEAR)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/stats/{SPORT}/regular/{YEAR}"
  )

def test_get_week_stats(client, mock_get):
  mock_get.return_value.json.return_value = {}

  client.get_week_stats(SPORT, "regular", YEAR, WEEK)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/stats/{SPORT}/regular/{YEAR}/{WEEK}"
  )

def test_get_projections(client, mock_get):
  mock_get.return_value.json.return_value = {}

  client.get_projections(SPORT, "regular", YEAR)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/projections/{SPORT}/regular/{YEAR}"
  )

def test_get_week_projections(client, mock_get):
  mock_get.return_value.json.return_value = {}

  client.get_week_projections(SPORT, "regular", YEAR, WEEK)

  mock_get.assert_called_once_with(
    f"https://api.sleeper.app/v1/projections/{SPORT}/regular/{YEAR}/{WEEK}"
  )





