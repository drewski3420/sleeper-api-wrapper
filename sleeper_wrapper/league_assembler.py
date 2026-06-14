from __future__ import annotations

from collections import defaultdict

from .all_players import AllPlayers
from .draft import Draft
from .matchup import Matchup
from .team import Team
from .transaction import FreeAgent, Trade, Transaction, Waiver
from .user import User


class LeagueAssembler:
  def __init__(self, client) -> None:
    self.client = client

  def assemble_league(self, league) -> None:
    league.users = self._get_users(league.league_id)
    league.users_by_id = {user.user_id: user for user in league.users}

    league.teams = self._get_teams(league.league_id, league.users_by_id)
    league.teams_by_user_id = {team.user.user_id: team for team in league.teams if team.user}
    league.teams_by_roster_id = {team.roster_id: team for team in league.teams}

    league.drafts = self._get_drafts(league.league_id, league.teams_by_user_id)

    league.sport_state = self._get_sport_state(league.sport)
    league.is_current_season = 1 if league.sport_state['league_season'] == league.season else 0

  def assemble_week_matchups(self, league, week: int) -> list[Matchup]:
    all_players = self._get_all_players(league)
    matchups = defaultdict(list)
    results = []

    matchup_data = self.client.get_league_matchups(league.league_id, week)
    matchup_data = sorted(matchup_data, key=lambda m: m['matchup_id'])

    for matchup_entry in matchup_data:
      matchups[matchup_entry["matchup_id"]].append(matchup_entry)

    for matchup_id, matchup_entries in matchups.items():
      matchup = Matchup(matchup_id=matchup_id, data=matchup_entries)
      for team_entry in matchup.teams:
        team_entry.team_obj = league.teams_by_roster_id[team_entry.roster_id]
        for player in team_entry.players_with_points:
          player['player'] = all_players.get_player(player['player_id'])
      results.append(matchup)

    return results

  def assemble_transactions(self, league, week: int) -> list[Transaction]:
    transactions = []
    transactions_data = self.client.get_league_transactions(league.league_id, week)
    all_players = self._get_all_players(league)

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

      self._enrich_transaction(transaction, league, all_players)
      transactions.append(transaction)

    return transactions

  def _enrich_transaction(self, transaction: Transaction, league, all_players: AllPlayers) -> None:
    for transaction_team in transaction.teams:
      team = league.teams_by_roster_id.get(transaction_team.roster_id)
      transaction_team.team = team
      transaction_team.user = team.user if team else None

      for transaction_player in transaction_team.players_added:
        transaction_player.player = all_players.get_player(transaction_player.player_id)

      for transaction_player in transaction_team.players_dropped:
        transaction_player.player = all_players.get_player(transaction_player.player_id)

  def _get_all_players(self, league) -> AllPlayers:
    if league.all_players is None:
      league.all_players = AllPlayers(season=league.season, sport=league.sport)
    return league.all_players

  def _get_users(self, league_id) -> list[User]:
    users_data = self.client.get_league_users(league_id)
    return [User(user_data.get('user_id'), user_data=user_data) for user_data in users_data]

  def _get_teams(self, league_id, users_by_id) -> list[Team]:
    teams_data = self.client.get_league_rosters(league_id)
    teams = []

    for team in teams_data:
      team['user'] = users_by_id.get(team.get("owner_id"))
      teams.append(Team(team))

    return teams

  def _get_drafts(self, league_id, teams_by_user_id) -> list[Draft]:
    drafts = self.client.get_league_drafts(league_id)
    return [Draft(draft.get('draft_id'), teams_by_user_id) for draft in drafts]

  def _get_sport_state(self, sport: str) -> dict:
    return self.client.get_sport_state(sport)
