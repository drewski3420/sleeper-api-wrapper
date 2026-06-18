# services/league_assembler.py
"""Assembly helpers for leagues, matchups, and transactions."""

from __future__ import annotations

from collections import defaultdict

from ..api_client import SleeperApiClient
from ..models.all_players import AllPlayers
from ..models.draft import Draft
from ..models.league import League
from ..models.matchup import Matchup
from ..models.team import Team
from ..models.transaction import FreeAgent, Trade, Transaction, Waiver
from ..models.user import User


class LeagueAssembler:
  """Build related league objects from API data."""

  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()

  def assemble_league(self, league: League) -> None:
    """Populate league users, teams, drafts, and state."""
    league.users = self._get_users(league.league_id)
    league.users_by_id = {user.user_id: user for user in league.users}

    league.teams = self._get_teams(league.league_id, league.users_by_id)
    league.teams_by_user_id = {
      team.user_obj.user_id: team for team in league.teams if team.user_obj
    }
    league.teams_by_roster_id = {team.roster_id: team for team in league.teams}

    all_players = self._get_all_players(league)
    league.all_players = all_players
    league.drafts = self._get_drafts(league.league_id)

    league.sport_state = self._get_sport_state(league.sport)
    league.is_current_season = (
      True if league.sport_state.get("league_season") == league.season else False
    )

  def assemble_week_matchups(self, league: League, week: int) -> list[Matchup]:
    """Build matchup objects for a given week."""
    all_players = self._get_all_players(league)
    matchups = defaultdict(list)
    results: list[Matchup] = []

    matchup_data = self.client.get_league_matchups(league.league_id, week)
    matchup_data = sorted(matchup_data, key=lambda m: m["matchup_id"])

    for matchup_entry in matchup_data:
      matchups[matchup_entry["matchup_id"]].append(matchup_entry)

    for matchup_id, matchup_entries in matchups.items():
      matchup = Matchup.from_payload(matchup_id=matchup_id, data=matchup_entries)

      for team_entry in matchup.teams:
        team_entry.team_obj = league.teams_by_roster_id.get(team_entry.roster_id)
        for matchup_player in team_entry.players_with_points:
          matchup_player.player_obj = all_players.get_player(matchup_player.player_id)
#        team_entry.sort_players_by_position()

      results.append(matchup)

    return results

  def assemble_week_transactions(self, league: League, week: int) -> list[Transaction]:
    transactions: list[Transaction] = []
    transactions_data = self.client.get_league_transactions(league.league_id, week)
    all_players = self._get_all_players(league)

    for item in transactions_data:
      item_type = item.get("type")

      if item_type == "trade":
        transaction = Trade.from_payload(item)
      elif item_type == "waiver":
        transaction = Waiver.from_payload(item)
      elif item_type == "free_agent":
        transaction = FreeAgent.from_payload(item)
      else:
        transaction = Transaction.from_payload(item)

      self._enrich_transaction(transaction, league, all_players)
      transactions.append(transaction)

    return transactions

  def _enrich_transaction(
    self,
    transaction: Transaction,
    league: League,
    all_players: AllPlayers,
  ) -> None:
    """Attach team, user, and player objects to a transaction."""
    for transaction_team in transaction.teams:
      team = league.teams_by_roster_id.get(transaction_team.roster_id)
      transaction_team.team_obj = team
      transaction_team.user_obj = team.user_obj if team else None

      for transaction_player in transaction_team.players_added:
        transaction_player.player_obj = all_players.get_player(transaction_player.player_id)

      for transaction_player in transaction_team.players_dropped:
        transaction_player.player_obj = all_players.get_player(transaction_player.player_id)

  def _get_all_players(self, league: League) -> AllPlayers:
    """Get or create the league player cache."""
    if league.all_players is None:
      league.all_players = AllPlayers(season=league.season, sport=league.sport)
    return league.all_players

  def _get_users(self, league_id: int) -> list[User]:
    """Fetch league users."""
    users_data = self.client.get_league_users(league_id)
    return [User(int(user_data.get("user_id")), user_data=user_data) for user_data in users_data]

  def _get_teams(self, league_id: int, users_by_id: dict[int, User]) -> list[Team]:
    """Fetch league teams."""
    teams_payload = self.client.get_league_rosters(league_id)
    teams_data = dict(teams_payload)
    teams = []

    for team in teams_data:
      owner_id = team.get("owner_id")
      team["user_obj"] = users_by_id.get(int(owner_id)) if owner_id is not None else None
      teams.append(Team(team))

    return teams

  def _get_drafts(
      self,
      league_id: int,
  ) -> list[Draft]:
    """Fetch league drafts."""
    drafts = self.client.get_league_drafts(league_id)
    return [
      Draft(
        int(draft.get("draft_id")),
        draft,
      )
        for draft in drafts
    ]

  def _get_sport_state(self, sport: str) -> dict:
    """Fetch sport state."""
    return self.client.get_sport_state(sport)
