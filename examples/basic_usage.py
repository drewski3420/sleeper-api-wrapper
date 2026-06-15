from sleeper_wrapper import League


def main() -> None:
  league_id = 123456789

  league = League(league_id)

  print(f"League: {league.league_name}")
  print(f"Season: {league.season}")
  print(f"Sport: {league.sport}")
  print(f"Teams: {league.num_teams}")
  print()

  print("Teams:")
  for team in league.teams:
    print(f"- {team.team_name}")
  print()

  week = league.first_week or 1
  print(f"Matchups for week {week}:")
  matchups = league.get_week_matchups(week)
  for matchup in matchups:
    print(matchup)


if __name__ == "__main__":
  main()
