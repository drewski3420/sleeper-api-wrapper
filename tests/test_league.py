"""Pytest tests for sleeper_wrapper.league."""

from __future__ import annotations

import sleeper_wrapper.league as league_module
from sleeper_wrapper.base_api import BaseApi
from sleeper_wrapper.league import League


class DummyClient:
  """Minimal client stub for league tests."""

  def __init__(self, league_data):
    """Initialize the dummy client.

    Args:
      league_data: League payload to return from get_league.
    """
    self._league_data = league_data
    self.get_league_calls = []

  def get_league(self, league_id):
    """Return the configured league payload.

    Args:
      league_id: League id requested.

    Returns:
      League payload.
    """
    self.get_league_calls.append(league_id)
    return self._league_data


class DummyAssembler:
  """Minimal assembler stub used to observe League behavior."""

  instances = []

  def __init__(self, client):
    """Initialize the assembler stub.

    Args:
      client: Shared API client.
    """
    self.client = client
    self.assemble_league_calls = []
    self.assemble_week_matchups_calls = []
    self.assemble_transactions_calls = []
    self.week_matchups_result = []
    self.transactions_by_week = {}
    DummyAssembler.instances.append(self)

  def assemble_league(self, league):
    """Record league assembly and populate minimal relationships.

    Args:
      league: League instance being assembled.
    """
    self.assemble_league_calls.append(league.league_id)
    league.users = []
    league.users_by_id = {}
    league.teams = []
    league.teams_by_user_id = {}
    league.teams_by_roster_id = {}
    league.drafts = []
    league.sport_state = {"league_season": league.season}
    league.is_current_season = 1

  def assemble_week_matchups(self, league, week):
    """Record matchup assembly call.

    Args:
      league: League instance.
      week: Week requested.

    Returns:
      Stub matchup list.
    """
    self.assemble_week_matchups_calls.append((league.league_id, week))
    return self.week_matchups_result

  def assemble_transactions(self, league, week):
    """Record transaction assembly call.

    Args:
      league: League instance.
      week: Week requested.

    Returns:
      Stub transaction list for the requested week.
    """
    self.assemble_transactions_calls.append((league.league_id, week))
    return self.transactions_by_week.get(week, [])


class DummyTransaction:
  """Minimal transaction stub for filtering tests."""

  def __init__(self, transaction_type):
    """Initialize the transaction stub.

    Args:
      transaction_type: Type string for the transaction.
    """
    self.transaction_type = transaction_type


def _build_league(league_data, monkeypatch):
  """Create a League with patched client and assembler.

  Args:
    league_data: League payload returned by the client.
    monkeypatch: Pytest monkeypatch fixture.

  Returns:
    Constructed League and the assembler instance used.
  """
  DummyAssembler.instances = []
  client = DummyClient(league_data)
  BaseApi.set_client(client)
  monkeypatch.setattr(league_module, "LeagueAssembler", DummyAssembler, raising=False)
  league = League(int(league_data["league_id"]))
  return league, DummyAssembler.instances[-1], client


class TestLeagueInitialization:
  """Tests for League initialization and core state."""

  def test_init_loads_league_data(self, league_data, restore_client, monkeypatch):
    """League should load raw league data on initialization."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assert league._data == league_data

  def test_init_sets_basic_attributes_from_payload(self, league_data, restore_client, monkeypatch):
    """League should set basic attributes from the API payload."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assert league.league_id == 289646328504385536
    assert league.season == "2018"
    assert league.sport == "nfl"
    assert league.scoring_settings == league_data["scoring_settings"]
    assert league.num_teams == 12
    assert league.league_status == "complete"
    assert league.league_name == "Sleeper Friends League"
    assert league.roster_positions == ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX", "FLEX", "DEF", "BN", "BN", "BN", "BN", "BN", "BN"]

  def test_init_sets_settings_derived_attributes(self, league_data, restore_client, monkeypatch):
    """League should set week and playoff attributes from settings."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assert league.settings == {
      "start_week": 2,
      "last_scored_leg": 16,
      "playoff_week_start": 14,
    }
    assert league.first_week == 2
    assert league.most_recent_week == 16
    assert league.playoff_start == 14

  def test_init_initializes_relationship_collections(self, league_data, restore_client, monkeypatch):
    """League should initialize empty relationship collections."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assert league.users == []
    assert league.users_by_id == {}
    assert league.teams == []
    assert league.teams_by_user_id == {}
    assert league.teams_by_roster_id == {}
    assert league.drafts == []
    assert league.all_players is None
    assert league.sport_state == {"league_season": "2018"}
    assert league.is_current_season == 1

  def test_init_initializes_transaction_cache(self, league_data, restore_client, monkeypatch):
    """League should initialize the transactions cache."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assert league.transactions == {}

  def test_init_invokes_league_assembler(self, league_data, restore_client, monkeypatch):
    """League should invoke LeagueAssembler during initialization."""
    league, assembler, client = _build_league(league_data, monkeypatch)

    assert client.get_league_calls == [289646328504385536]
    assert assembler.client is client
    assert assembler.assemble_league_calls == [league.league_id]

  def test_str_returns_readable_summary(self, league_data, restore_client, monkeypatch):
    """League.__str__ should return a readable summary."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assert str(league) == "12 Team League: Sleeper Friends League (ID 289646328504385536)"


class TestLeagueDataFetching:
  """Tests for League data-fetching methods."""

  def test_get_data_returns_client_payload(self, league_data, restore_client, monkeypatch):
    """_get_data should return the payload from the API client."""
    league, _, client = _build_league(league_data, monkeypatch)

    result = league._get_data()

    assert result == league_data
    assert client.get_league_calls == [289646328504385536, 289646328504385536]

  def test_get_results_returns_empty_when_week_bounds_missing(self, league_data, restore_client, monkeypatch):
    """get_results should return empty mapping when week bounds are unavailable."""
    league_data = {
      **league_data,
      "settings": {
        "start_week": None,
        "last_scored_leg": None,
        "playoff_week_start": 14,
      },
    }
    league, _, _ = _build_league(league_data, monkeypatch)

    results = league.get_results()

    assert dict(results) == {}

  def test_get_results_fetches_each_week_in_range(self, league_data, restore_client, monkeypatch):
    """get_results should fetch matchups for each scored week."""
    league, _, _ = _build_league(league_data, monkeypatch)

    calls = []

    def fake_get_week_matchups(week):
      calls.append(week)
      return [f"week-{week}"]

    monkeypatch.setattr(league, "get_week_matchups", fake_get_week_matchups)

    results = league.get_results()

    assert calls == list(range(2, 17))
    assert dict(results) == {
      2: ["week-2"],
      3: ["week-3"],
      4: ["week-4"],
      5: ["week-5"],
      6: ["week-6"],
      7: ["week-7"],
      8: ["week-8"],
      9: ["week-9"],
      10: ["week-10"],
      11: ["week-11"],
      12: ["week-12"],
      13: ["week-13"],
      14: ["week-14"],
      15: ["week-15"],
      16: ["week-16"],
    }

  def test_get_week_matchups_delegates_to_assembler(self, league_data, restore_client, monkeypatch):
    """get_week_matchups should delegate matchup assembly to LeagueAssembler."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assembler = DummyAssembler.instances[-1]
    assembler.week_matchups_result = ["matchup-a", "matchup-b"]

    result = league.get_week_matchups(2)

    newest_assembler = DummyAssembler.instances[-1]
    assert result == ["matchup-a", "matchup-b"]
    assert newest_assembler.assemble_week_matchups_calls == [(289646328504385536, 2)]

  def test_get_transactions_populates_cache_for_new_week(self, league_data, restore_client, monkeypatch):
    """_get_transactions should populate cache for an unfetched week."""
    league, _, _ = _build_league(league_data, monkeypatch)

    assembler = DummyAssembler.instances[-1]
    assembler.transactions_by_week[5] = [DummyTransaction("trade")]

    result = league._get_transactions(5)

    newest_assembler = DummyAssembler.instances[-1]
    assert len(DummyAssembler.instances) == 2
    assert newest_assembler.assemble_transactions_calls == [(289646328504385536, 5)]
    assert league.transactions[5] == result

  def test_get_transactions_reuses_cache_for_existing_week(self, league_data, restore_client, monkeypatch):
    """_get_transactions should reuse cached transactions for a week."""
    league, _, _ = _build_league(league_data, monkeypatch)
    cached_transactions = [DummyTransaction("trade")]
    league.transactions[7] = cached_transactions
    initial_instance_count = len(DummyAssembler.instances)

    result = league._get_transactions(7)

    assert result == cached_transactions
    assert len(DummyAssembler.instances) == initial_instance_count

  def test_get_transactions_filters_by_transaction_type(self, league_data, restore_client, monkeypatch):
    """_get_transactions should filter transactions by requested type."""
    league, _, _ = _build_league(league_data, monkeypatch)
    league.transactions[4] = [
      DummyTransaction("trade"),
      DummyTransaction("waiver"),
      DummyTransaction("free_agent"),
    ]

    result = league._get_transactions(4, "waiver")

    assert len(result) == 1
    assert result[0].transaction_type == "waiver"

  def test_get_transactions_returns_all_for_all_type(self, league_data, restore_client, monkeypatch):
    """_get_transactions should return all transactions for type All."""
    league, _, _ = _build_league(league_data, monkeypatch)
    league.transactions[4] = [
      DummyTransaction("trade"),
      DummyTransaction("waiver"),
    ]

    result = league._get_transactions(4, "All")

    assert result == league.transactions[4]

  def test_get_trades_returns_trade_transactions(self, league_data, restore_client, monkeypatch):
    """get_trades should request trade transactions."""
    league, _, _ = _build_league(league_data, monkeypatch)

    calls = []

    def fake_get_transactions(week, transaction_type="All"):
      calls.append((week, transaction_type))
      return ["trade-result"]

    monkeypatch.setattr(league, "_get_transactions", fake_get_transactions)

    result = league.get_trades(8)

    assert result == ["trade-result"]
    assert calls == [(8, "trade")]

  def test_get_waivers_returns_waiver_transactions(self, league_data, restore_client, monkeypatch):
    """get_waivers should request waiver transactions."""
    league, _, _ = _build_league(league_data, monkeypatch)

    calls = []

    def fake_get_transactions(week, transaction_type="All"):
      calls.append((week, transaction_type))
      return ["waiver-result"]

    monkeypatch.setattr(league, "_get_transactions", fake_get_transactions)

    result = league.get_waivers(9)

    assert result == ["waiver-result"]
    assert calls == [(9, "waiver")]

  def test_get_free_agents_returns_free_agent_transactions(self, league_data, restore_client, monkeypatch):
    """get_free_agents should request free_agent transactions."""
    league, _, _ = _build_league(league_data, monkeypatch)

    calls = []

    def fake_get_transactions(week, transaction_type="All"):
      calls.append((week, transaction_type))
      return ["free-agent-result"]

    monkeypatch.setattr(league, "_get_transactions", fake_get_transactions)

    result = league.get_free_agents(10)

    assert result == ["free-agent-result"]
    assert calls == [(10, "free_agent")]
