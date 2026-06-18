from sleeper_wrapper.services.league_assembler import LeagueAssembler
from sleeper_wrapper.models.league import League
from sleeper_wrapper.base_api import BaseApi

from fixtures import TEST_LEAGUE_SCENARIO
from test_classes import FakeSleeperApiClient

scenario = TEST_LEAGUE_SCENARIO
week = scenario['sport_state']['week']

client = FakeSleeperApiClient(scenario)
assembler = LeagueAssembler(client)

league = League(league_data=scenario)
assembler.assemble_league(league)


def test_assemble_league():
  # ---- core invariants ----
  # league ID
  assert str(league.league_id) == scenario["league_id"]

  # users
  assert len(league.users) == len(scenario["users"])

  # rosters/teams (depending on your mapping)
  assert len(league.teams) == len(scenario["rosters"])

  # drafts
  assert len(league.drafts) == len(scenario["drafts"])

def test_assemble_transactions():

  transactions = assembler.assemble_week_transactions(league, week)
  assert len(transactions) == len(scenario["transactions"])

def test_assemble_week_matchups():

  # matchups
  matchups = assembler.assemble_week_matchups(league,week)
  assert len(matchups) == len(scenario['matchups']) / 2

if __name__ == '__main__':
  test_assemble_transactions()
  test_assemble_week_matchups()
