from sleeper_wrapper.assembler import LeagueAssembler
from sleeper_wrapper.league import League
from sleeper_wrapper.base_api import BaseApi

from fixtures import TEST_LEAGUE_SCENARIO

class FakeClient:
  def __init__(self, fixture):
    self.fixture = fixture

  def get_league_users(self, league_id):
    return self.fixture["users"]

  def get_league_rosters(self, league_id):
    return self.fixture["rosters"]

  def get_league_drafts(self, league_id):
    return self.fixture["drafts"]

  def get_draft_picks(self, league_id):
    return self.fixture["draft_picks"]

  def get_draft_traded_picks(self, league_id):
    return self.fixture["draft_picks"]

  def get_draft(self, league_id):
    return self.fixture['drafts'][0]

  def get_league_matchups(self, league_id, week):
    return self.fixture["matchups"]

  def get_league_transactions(self, league_id, week):
    return self.fixture["transactions"]

  def get_league(self, league_id):
    return self.fixture

  def get_players(self, sport: str, season: str):
    return self.fixture['players']

  def get_sport_state(self, sport: str):
    return self.fixture['sport_state']

scenario = TEST_LEAGUE_SCENARIO

client = FakeClient(scenario)
BaseApi.set_client(client=FakeClient(scenario))
assembler = LeagueAssembler()

league = League(league_id=scenario["league_id"])
assembler.assemble_league(league)


def test_assemble_league():
  # ---- core invariants ----

  assert str(league.league_id) == scenario["league_id"]

  # users
  assert len(league.users) == len(scenario["users"])

  # rosters/teams (depending on your mapping)
  assert len(league.teams) == len(scenario["rosters"])

  # drafts
  assert len(league.drafts) == len(scenario["drafts"])

def test_assemble_transactions():

  week = scenario['sport_state']['week']
  transactions = league.get_all_transactions(week)
  assert len(transactions) == len(scenario["transactions"])

  trades = league.get_trades(week)
  assert len(trades) == len([s for s in scenario["transactions"] if s['type'] == 'trade'])

  free_agents = league.get_free_agents(week)
  assert len(free_agents) == len([s for s in scenario["transactions"] if s['type'] == 'free_agent'])

  waivers = league.get_waivers(week)
  assert len(waivers) == len([s for s in scenario["transactions"] if s['type'] == 'waiver'])

def test_assemble_week_matchups():

  # matchups
  assert len(league.get_week_matchups(16)) == len(scenario['matchups']) / 2


