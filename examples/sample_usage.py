"""Sample usage script for the sleeper_wrapper package."""

from __future__ import annotations

from sleeper_wrapper import (
  AllPlayers,
  DraftService,
  LeagueService,
  UserService,
)

# Replace these ids with real values for your account/league/draft.
sport = "nfl"
season = 2018
user_name = "calamariota757"
league_id = 289646328504385536
draft_id = 289646328508579840
week = 1

def print_user_summary(user_service: UserService, user_name: str, season: int, sport: str) -> None:
  """Load a user and print related league and draft info."""
  print("=== User Summary ===")
  user = user_service.load_user(user_name)
  user_id = user.user_id
  print(user)

  leagues = user_service.get_all_leagues(user_id=user_id, season=season, sport=sport)
  print(f"Leagues found: {len(leagues)}")
  for league in leagues:
    print(f"- {league}")

  drafts = user_service.get_all_drafts(user_id=user_id, season=season, sport=sport)
  print(f"Drafts found: {len(drafts)}")
  for draft in drafts:
    print(f"- {draft}")

  print()

def print_league_summary(league_service: LeagueService, league_id: int, week: int) -> None:
  """Load a league and print matchup and transaction info."""
  print("=== League Summary ===")
  league = league_service.load_league(league_id)
  print(league)
  print(f"Users: {len(league.users)}")
  print(f"Teams: {len(league.teams)}")
  print(f"Drafts: {len(league.drafts)}")
  print(f"Current season flag: {league.is_current_season}")
  print()

  print(f"=== Week {week} Matchups ===")
  matchups = league_service.get_week_matchups(league, week)
  print(f"Matchups found: {len(matchups)}")
  for matchup in matchups:
    print(f"Matchup {matchup.matchup_id}")
    for team in matchup.teams:
      team_name = team.team_obj.team_name if team.team_obj else f"Roster {team.roster_id}"
      print(
        f"  - {team_name}: "
        f"{team.points} pts "
        f"(starters: {team.starter_points}, bench: {team.bench_points})"
      )
    if matchup.winning_team is not None:
      winner_name = (
        matchup.winning_team.team_obj.team_name
        if matchup.winning_team.team_obj
        else f"Roster {matchup.winning_team.roster_id}"
      )
      print(f"  Winner: {winner_name}")
    print()

  print(f"=== Week {week} Transactions ===")
  transactions = league_service.get_week_transactions(league, week)
  print(f"Transactions found: {len(transactions)}")
  for transaction in transactions[:10]:
    print(
      f"- Transaction {transaction.transaction_id} "
      f"type={transaction.transaction_type} "
      f"status={transaction.status}"
    )
    for transaction_team in transaction.teams:
      team_name = (
        transaction_team.team_obj.team_name
        if transaction_team.team_obj
        else f"Roster {transaction_team.roster_id}"
      )
      print(f"  Team: {team_name}")

      if transaction_team.players_added:
        added = ", ".join(str(player.player_obj or player.player_id) for player in transaction_team.players_added)
        print(f"    Added: {added}")

      if transaction_team.players_dropped:
        dropped = ", ".join(str(player.player_obj or player.player_id) for player in transaction_team.players_dropped)
        print(f"    Dropped: {dropped}")

      if transaction_team.picks_added:
        picks_added = ", ".join(
          f"{pick.season} round {pick.round_number}" for pick in transaction_team.picks_added
        )
        print(f"    Picks added: {picks_added}")

      if transaction_team.picks_lost:
        picks_lost = ", ".join(
          f"{pick.season} round {pick.round_number}" for pick in transaction_team.picks_lost
        )
        print(f"    Picks lost: {picks_lost}")

  print()


def print_draft_summary(draft_service: DraftService, draft_id: int) -> None:
  """Load a draft and print pick info."""
  print("=== Draft Summary ===")
  draft = draft_service.load_draft(draft_id)
  print(draft)

  picks = draft_service.get_all_picks(draft_id)
  print(f"Total picks: {len(picks)}")
  for pick in picks[:10]:
    print(f"- {pick}")

  traded_picks = draft_service.get_all_traded_picks(draft_id)
  print(f"Traded picks: {len(traded_picks)}")
  for pick in traded_picks[:10]:
    print(f"- {pick}")

  print()

def print_players_summary(season: int, sport: str) -> None:
  """Load cached player data and print a few examples."""
  print("=== Players Summary ===")
  players = AllPlayers(season=season, sport=sport)
  players_by_id = players.players_by_id
  print(f"Players loaded: {len(players_by_id)}")

  sample_ids = list(players_by_id.keys())[:5]
  for player_id in sample_ids:
    print(f"- {players.get_player(player_id)}")

  print()

def main() -> None:
  """Run a simple sample flow against the Sleeper API."""
  user_service = UserService()
  league_service = LeagueService()
  draft_service = DraftService()

  print_user_summary(user_service, user_name=user_name, season=season, sport=sport)
  print_league_summary(league_service, league_id=league_id, week=week)
  print_draft_summary(draft_service, draft_id=draft_id)
  print_players_summary(season=season, sport=sport)

if __name__ == "__main__":
  main()
