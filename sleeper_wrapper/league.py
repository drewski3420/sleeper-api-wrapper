from typing import Union
from collections import defaultdict

from .base_api import BaseApi
from .stats import Stats
from .draft import Draft
from .team import Team
from .user import User
from .matchup import Matchup
from .all_players import AllPlayers
from .player import Player
from .transaction import Transaction, Waiver, FreeAgent, Trade

class League(BaseApi):
  def __init__(self, league_id: Union[str, int]) -> None:
    self.league_id = league_id
    self._base_url = "https://api.sleeper.app/v1/league/{}".format(self.league_id)
    self._data = self._get_data()
    self.season = self._data.get('season')
    self.sport = self._data.get('sport')
    self.settings = self._data.get('settings')
    self.scoring_settings = self._data.get('scoring_settings')
    self.first_week = self.settings.get('start_week')
    self.most_recent_week = self.settings.get('last_scored_leg')
    self.playoff_start = self.settings.get('playoff_week_start')
    self.num_teams = self._data.get('total_rosters')
    self.league_status = self._data.get('status')
    self.league_name = self._data.get('name')
    self.users = self._get_users()
    self.users_by_id = {user['user_id']: user for user in self.users}
    self.teams = self._get_teams()
    self.teams_by_user_id ={team.user['user_id']: team for team in self.teams}
    self.teams_by_roster_id ={team.roster_id: team for team in self.teams}
    self.drafts = self._get_drafts()
    self.all_players = None
    self.sport_state = self._get_sport_state()
    self.is_current_season = (1 if self.sport_state['league_season'] == self.season else 0 )
    self.transactions = {}

  def __str__(self):
    return f"{self.num_teams} Team League: {self.league_name} (ID {self.league_id})"

  def _get_data(self) -> dict:
    return self._call(self._base_url)

  def _get_drafts(self) -> list:
    drafts = self._call("{}/{}".format(self._base_url, "drafts"))
    return [Draft(draft.get('draft_id'), self.teams_by_user_id) for draft in drafts]

  def _get_teams(self) -> list:
    teams_data = self._call("{}/{}".format(self._base_url,"rosters"))

    teams = []
    for team in teams_data:
      user_info = self.users_by_id.get(team["owner_id"])

      if user_info:
        team['user'] = user_info
      else:
        team['user'] = None

      teams.append(Team(team))

    return teams

  def _get_users(self) -> list:
    users = self._call("{}/{}".format(self._base_url,"users"))
    return users

  def get_results(self) -> list:
    r = defaultdict()
    for week in range(self.first_week, self.most_recent_week + 1):
      r[week] = self.get_week_matchups(week)
    return r

  def get_week_matchups(self, week: int) -> list:
    self.all_players = AllPlayers(season=self.season,sport=self.sport)
    matchups = defaultdict(list)
    r = []
    matchup_data = self._call("{}/{}/{}".format(self._base_url,"matchups", week))
    matchup_data = sorted(matchup_data, key=lambda m: m['matchup_id'])
    for m in matchup_data:
      matchups[m["matchup_id"]].append(m)

    for matchup_id, m in matchups.items():
      matchup = Matchup(matchup_id=matchup_id, data=m)
      for t in matchup.teams:
        t.team_obj = self.teams_by_roster_id[t.roster_id]
        for player in t.players_with_points:
          player['player'] = self.all_players.get_player(player['player_id'])
      r.append(matchup)
    return r

  def _get_sport_state(self) -> dict:
    return BaseApi()._call(f"https://api.sleeper.app/v1/state/{self.sport}")

  def get_transactions(self, week: int, transaction_type: str = "All") -> list[Transaction]:
    print(f"Getting transactions for Week {week}, current len is {sum(len(l) for l in self.transactions.values())}")

    if week not in self.transactions.keys():
      self.transactions[week] = []
      transactions_data = self._call("{}/{}/{}".format(self._base_url,"transactions", week))

      for item in transactions_data:
        item_type = item.get("type")

        if item_type == "trade":
          transaction = Trade(item)

        elif item_type == "waiver":
          transaction = Waiver(item)

        elif item_type == "free_agent":
          transaction = FreeAgent(item)

        else:
          transaction = Transaction(item)

        self.transactions[week].append(transaction)

    return [t for t in self.transactions if transaction_type in [t.transaction_type,"All"]]

  def get_trades(self, week: int) -> list:
    return self.get_transactions(week, "trade")

  def get_waivers(self, week: int) -> list:
    return self.get_transactions(week, "waiver")

  def get_free_agents(self, week: int) -> list:
    return self.get_transactions(week, "free_agent")

#
#  def get_playoff_winners_bracket(self) -> list:
#    """Retrieves the winner's playoff bracket."""
#    return self._call("{}/{}".format(self._base_url,"winners_bracket"))
#
#  def get_playoff_losers_bracket(self) -> list:
#    """Retrieves the loser's playoff bracket."""
#    return self._call("{}/{}".format(self._base_url,"losers_bracket"))
#

#  def get_traded_picks(self) -> list:
#    """Retrieves the league's traded draft picks."""
#    return self._call("{}/{}".format(self._base_url,"traded_picks"))

#  def get_standings(self, rosters: list, users: list) -> dict:
#    """Creates standings based on the team's wins, losses, and ties.
#
#    Args:
#      rosters: 
#        List of rosters for the league.
#      users: list
#        List of user IDs for the league.
#
#    Returns:
#      List of tuples (team_name, wins, losses, points) sorted by wins in
#      descending order.
#    """
#    users_dict = self.map_users_to_team_name(users)
#
#    roster_standings_list = []
#    for roster in rosters:
#      wins = roster["settings"]["wins"]
#      points = roster["settings"]["fpts"]
#      name = roster["owner_id"]
#      losses = roster["settings"]["losses"]
#      if name is not None:
#        roster_tuple = (wins, losses, points, users_dict[name])
#      else:
#        roster_tuple = (wins, losses, points, None)
#      roster_standings_list.append(roster_tuple)
#
#    roster_standings_list.sort(reverse = 1)
#
#    clean_standings_list = []
#    for item in roster_standings_list:
#      clean_standings_list.append((item[3], str(item[0]), str(item[1]), str(item[2])))
#    
#    return clean_standings_list

#  def get_scoreboards(self, rosters: list, matchups: list, users: list, score_type: str, season: Union[str, int], week: Union[str, int]) -> Union[dict, None]:
#    """Returns the team names and scores from each matchup.
#
#    Uses the provided information about the league to create a scoreboard
#    for the given week. It pulls data from the rosters and users to find
#    the team name and then pulls the team's score. It does not currently
#    support leagues with custom scoring options and relies on the `Stats()`
#    class, which is no longer officially documented by Sleeper.
#
#    Args:
#      rosters: list
#        List of rosters for the league.
#      matchups: list
#        List of matchups for that week.
#      users: list
#        List of users for the league.
#      score_type: str
#        Scoring type for the league, eg "pts_std", "pts_ppr", or "pts_half_ppr"
#      season: Union[str, int]
#        The season to retrieve the scoreboards. May be provided as either a
#        str or an int.
#      week: Union[str, int]
#        The week to retrieve the scoreboards. May be provided as either a
#        str or an int.
#
#    Returns:
#      A dict with the matchup ID as key and the corresponding teams' names
#      and scores for that matchup.
#    """
#    roster_id_dict = self.map_rosterid_to_ownerid(rosters)
#
#    if len(matchups) == 0:
#      return None
#
#    # Get the users to team name stats
#    users_dict = self.map_users_to_team_name(users)
#
#    # Map roster_id to points
#    scoreboards_dict = {}
#
#    for team in matchups:
#      matchup_id = team["matchup_id"]
#      current_roster_id = team["roster_id"]
#      owner_id = roster_id_dict[current_roster_id]
#      if owner_id is not None:
#        team_name = users_dict[owner_id]
#      else:
#        team_name = "Team name not available"
#
#      team_score = self.get_team_score(team["starters"], score_type, season, week)
#      if team_score is None:
#        team_score = 0
#
#      team_score_tuple = (team_name, team_score)
#      if matchup_id not in scoreboards_dict:
#        scoreboards_dict[matchup_id] = [team_score_tuple]
#      else:
#        scoreboards_dict[matchup_id].append(team_score_tuple)
#    return scoreboards_dict

#  def get_close_games(self, scoreboards: list, close_num: float) -> dict:
#    """Returns scoreboard's games where final margin is beneath given number.
#
#    Args:
#      scoreboards: list
#        List of scoreboards, which can be retrieved with the
#        `get_scoreboards()` method.
#      close_num: float
#        The final margin to use as a threshold for determining close games.
#
#    Returns:
#      A dict of matchups qualifying as close.
#    """
#    close_games_dict = {}
#    for key in scoreboards:
#      team_one_score = scoreboards[key][0][1]
#      team_two_score = scoreboards[key][1][1]
#
#      if abs(team_one_score-team_two_score) < close_num:
#        close_games_dict[key] = scoreboards[key]
#    return close_games_dict

#  def get_team_score(self, starters: list, score_type: str, season: Union[str, int], week: Union[str, int]) -> float:
#    """Retrieves a team's scores for a week based on the score type.
#
#    Uses the provided list of starters to pull their stats for that week
#    with the given score type. It does not currently support leagues with
#    custom scoring options because it pulls the pre-calculated score based
#    on score type and does not calculate the score based on the league's
#    scoring setting. It relies on the `Stats()` class to do this, which is 
#    no longer officially documented by Sleeper.
#
#    Args:
#      starters: list
#        A list of starters for the team.
#      score_type: str
#        Scoring type for the league, eg "pts_std", "pts_ppr", or "pts_half_ppr"
#      season: Union[str, int]
#        The season to retrieve the scores. May be provided as either a str 
#        or an int.
#      week: Union[str, int]
#        The week to retrieve the scores. May be provided as either a str or
#        an int.
#
#    Returns:
#      The total score as a float for the team in that week.
#    """
#    total_score = 0
#    stats = Stats()
#    week_stats = stats.get_week_stats("regular", season, week)
#    for starter in starters:
#      if stats.get_player_week_stats(week_stats, starter) is not None:
#        try:
#          total_score += stats.get_player_week_stats(week_stats, starter)[score_type]
#        except KeyError:
#          total_score += 0
#
#    return total_score
#
#  def empty_roster_spots(self, user_id: Union[str, int]) -> Union[int, None]:
#    """Returns the number of empty roster spots on a user's team.
#
#    Args:
#      user_id: Union[str, int]
#        The user's ID to check for empty roster spots.
#
#    Returns:
#      The number of empty roster spots assuming the user was found. Otherwise
#      returns `None`.
#    """
#    # get size of maximum roster
#    max_roster_size = len(self._league["roster_positions"])
#
#    # finds roster of user, returns max size - size of user roster
#    rosters = self.get_rosters()
#    for roster in rosters:
#      if user_id == roster["owner_id"]:
#        return max_roster_size - len(roster["players"])
#
#    # returns None if user was not found
#    return None
#
#
#  def get_league_name(self) -> str:
#    """Returns name of league."""
#    return self._league["name"]
#
#  def get_negative_scores(self, week: Union[str, int]) -> None:
#    pass
#
#  def get_rosters_players(self) -> None:
#    pass


