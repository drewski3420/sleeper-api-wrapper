class FakeSleeperApiClient:
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

class FakeAllPlayers:
  def __init__(self, players_by_id=None):
    self.players_by_id = players_by_id or {}

  def get_player(self, player_id):
    return self.players_by_id.get(str(player_id))

class FakeFileCache:
  def __init__(self, data=None):
    self.data = data
    self.written = None

  def read_or_none(self):
    return self.data

  def write_json(self, data):
    self.written = data

  def exists(self):
    return self.data is not None

class FakeLeagueAssembler:
  def __init__(self):
    self.assembled_league = None
    self.week_matchups_calls = []
    self.transactions_calls = []

  def assemble_league(self, league):
    self.assembled_league = league

  def assemble_week_matchups(self, league, week):
    self.week_matchups_calls.append((league, week))
    return []

  def assemble_transactions(self, league, week):
    self.transactions_calls.append((league, week))
    return []

class FakePlayerRepository:
  def __init__(self, players_by_id=None):
    self.players_by_id = players_by_id or {}
    self.get_player_calls = []

  def load_players_by_id(self):
    return self.players_by_id

  def get_player(self, player_id):
    self.get_player_calls.append(player_id)
    return self.players_by_id.get(str(player_id))
