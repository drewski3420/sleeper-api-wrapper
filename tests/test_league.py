from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path

import pytest

from sleeper_wrapper import League


def _load_test_config() -> dict:
    config_path = Path(__file__).resolve().parent / "local_test_config.json"
    if not config_path.exists():
        pytest.skip(
            "Missing tests/local_test_config.json. Copy tests/local_test_config.example.json "
            "to tests/local_test_config.json and fill in your local values."
        )

    try:
        with config_path.open(encoding="utf-8") as config_file:
            return json.load(config_file)
    except JSONDecodeError:
        pytest.skip(
            "Invalid JSON in tests/local_test_config.json. "
            "Fix the file contents before running integration tests."
        )


def _get_league_id() -> int | str:
    config = _load_test_config()
    league_id = config.get("league_id")
    if league_id is None:
        pytest.skip("Missing 'league_id' in tests/local_test_config.json")
    return league_id


def _get_scoreboard_league_id() -> int | str:
    config = _load_test_config()
    league_id = config.get("scoreboard_league_id", config.get("league_id"))
    if league_id is None:
        pytest.skip("Missing 'scoreboard_league_id' or 'league_id' in tests/local_test_config.json")
    return league_id


def test_get_league() -> None:
    """Tests the get_league method."""
    league_id = _get_league_id()
    league = League(league_id)
    league_info = league.get_league()

    assert isinstance(league_info, dict)
    assert str(league_info["league_id"]) == str(league_id)


def test_get_rosters() -> None:
    """Tests the get_rosters method."""
    league = League(_get_league_id())
    rosters = league.get_rosters()

    assert isinstance(rosters, list)
    assert len(rosters) > 5


def test_get_users() -> None:
    """Tests the get_users method."""
    league = League(_get_league_id())
    users = league.get_users()

    assert isinstance(users, list)
    assert isinstance(users[0]["user_id"], str)
    # I guess username is not a thing


def test_get_matchups() -> None:
    """Tests the get_matchups method."""
    league = League(_get_league_id())
    matchup_info = league.get_matchups(4)
    first_item = matchup_info[0]
    assert isinstance(matchup_info, list)
    assert isinstance(first_item, dict)

    matchup_info = league.get_matchups(20)

    assert len(matchup_info) == 0


def test_get_playoff_winners_bracket() -> None:
    """Tests the get_playoff_winners_bracket method."""
    league = League(_get_league_id())
    bracket = league.get_playoff_winners_bracket()
    first_item = bracket[0]

    assert isinstance(bracket, list)
    assert isinstance(first_item, dict)


def test_get_playoff_losers_bracket() -> None:
    """Tests the get_playoff_losers method."""
    league = League(_get_league_id())
    bracket = league.get_playoff_losers_bracket()
    first_item = bracket[0]

    assert isinstance(bracket, list)
    assert isinstance(first_item, dict)


def test_get_transactions() -> None:
    """Tests the get_transactions method.

    Note: Not really sure whether this method works or what its supposed
    to do yet because the season has not fully started.
    """
    league = League(_get_league_id())
    transactions = league.get_transactions(4)
    assert isinstance(transactions, list)

    transactions = league.get_transactions("4")
    assert isinstance(transactions, list)


def test_get_trades() -> None:
    """Tests the get_trades method.

    Note: It would be better if we had trades to verify!
    """
    league = League(_get_league_id())
    trades = league.get_trades(4)
    assert isinstance(trades, list)
    assert len(trades) == 0


def test_get_waivers() -> None:
    """Tests the get_waivers method.

    Note: It would be better if we had waivers to verify!
    """
    league = League(_get_league_id())
    waivers = league.get_waivers(4)
    assert isinstance(waivers, list)
    assert len(waivers) == 0


def test_get_free_agents() -> None:
    """Tests the get_free_agents method.

    Note: It would be better if we had free agents to verify!
    """
    league = League(_get_league_id())
    free_agents = league.get_free_agents(4)
    assert isinstance(free_agents, list)
    assert len(free_agents) == 0


def test_get_traded_picks() -> None:
    """Tests the get_traded_picks method."""
    league = League(_get_league_id())
    traded_picks = league.get_traded_picks()
    first_item = traded_picks[0]

    assert isinstance(traded_picks, list)
    assert isinstance(first_item, dict)


def test_get_all_drafts() -> None:
    league = League(_get_league_id())
    drafts = league.get_all_drafts()
    first_item = drafts[0]

    assert isinstance(drafts, list)
    assert isinstance(first_item, dict)


def test_get_standings() -> None:
    """Tests the get_standings method."""
    league = League(_get_league_id())
    rosters = league.get_rosters()
    users = league.get_users()
    standings = league.get_standings(rosters, users)
    first_item = standings[0]

    assert isinstance(first_item, tuple)
    assert len(standings) == 12


def test_get_scoreboards() -> None:
    """Tests the get_scoreboards method.

    Needs more testing after the season starts.
    """
    league = League(_get_scoreboard_league_id())
    matchups = league.get_matchups(1)
    users = league.get_users()
    rosters = league.get_rosters()
    scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", 2019, 1)
    print(scoreboards)
    assert isinstance(scoreboards, dict)


def test_get_close_games() -> None:
    """Tests the get_close_games method.

    Notes: Need to test more.
    """
    league = League(_get_scoreboard_league_id())
    matchups = league.get_matchups(1)
    users = league.get_users()
    rosters = league.get_rosters()
    scoreboards = league.get_scoreboards(rosters, matchups, users, "pts_half_ppr", 2019, 1)
    close_games = league.get_close_games(scoreboards, 10)
    assert isinstance(close_games, dict)


def test_empty_roster_spots() -> None:
    """Tests the empty_roster_spots method.

    Assertion 1: ensures that our function returns an integer for all league users
    (and not None)

    Assertion 2: ensures that our function returns None when an invalid user id is sent
    """
    league = League(_get_scoreboard_league_id())
    users = league.get_users()
    rosters = league.get_rosters()
    # Assertion 1
    for user in users:
        user_id = user["user_id"]
        for roster in rosters:
            if user_id == roster["owner_id"]:
                assert league.empty_roster_spots(user_id) is not None

    # Assertion 2
    assert league.empty_roster_spots(-10000) is None


def test_get_negative_scores() -> None:
    pass


@pytest.mark.skip(reason="Legacy test targets removed BaseApi._call implementation.")
def test_get_sport_state() -> None:
    pass
