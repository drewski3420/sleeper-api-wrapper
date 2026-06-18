# Sleeper API Wrapper

A Python wrapper for working with the Sleeper API. This package includes:

- A low-level API client for direct endpoint access
- Python models for Sleeper resources
- Service classes for loading richer league, draft, and user data
- Optional local JSON caching for player data [3][13][14]

---

## Package Exports

The package publicly exports the following top-level objects [3]:

- `SleeperApiClient`
- `BaseApi`
- `AllPlayers`
- `Draft`
- `League`
- `Matchup`
- `MatchupPlayer`
- `MatchupTeam`
- `Pick`
- `TradedPick`
- `Player`
- `Team`
- `Transaction`
- `TransactionPick`
- `TransactionPlayer`
- `TransactionTeam`
- `Trade`
- `FreeAgent`
- `Waiver`
- `User`
- `FileCache`
- `PlayerRepository`
- `DraftService`
- `LeagueAssembler`
- `LeagueService`
- `UserService`

Example import:

```python
from sleeper_wrapper import SleeperApiClient, LeagueService, UserService
```

---

## Project Structure

```text
sleeper_wrapper/
├── api_client.py
├── base_api.py
├── __init__.py
├── models/
│   ├── all_players.py
│   ├── draft.py
│   ├── league.py
│   ├── matchup.py
│   ├── pick.py
│   ├── player.py
│   ├── team.py
│   ├── transaction.py
│   └── user.py
├── repositories/
│   ├── file_cache.py
│   └── player_repository.py
└── services/
    ├── draft_service.py
    ├── league_assembler.py
    ├── league_service.py
    └── user_service.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/drewski3420/sleeper-api-wrapper.git
cd sleeper-api-wrapper
```

Install required dependencies if needed:

```bash
pip install requests
```

If the repository includes packaging config, install it in editable mode:

```bash
pip install -e .
```

If not, you can still use it from the project directory directly.

---

## Quick Start

### Direct API access

`BaseApi` provides a shared client and will create a `SleeperApiClient` automatically if one is not supplied [2].

```python
from sleeper_wrapper import SleeperApiClient

client = SleeperApiClient()
league = client.get_league(123456789)
print(league)
```

### Service-based usage

```python
from sleeper_wrapper import LeagueService

service = LeagueService()
league = service.load_league(123456789)

print(league.league_name)
print(league.teams)
```

`LeagueService.load_league()` fetches the league and then assembles related objects [17].

---

## Core Components

## `SleeperApiClient`

This is the main low-level client for hitting Sleeper endpoints.

### Supported methods

Based on the available code, the client supports at least:

- `get_league_drafts(league_id)` → fetch draft payloads for a league [1]
- `get_league_matchups(league_id, week)` → fetch matchup payloads for a week [1]
- `get_league_transactions(league_id, week)` → fetch transaction payloads for a week [1]
- `get_draft(draft_id)` → fetch a draft [1]
- `get_draft_picks(draft_id)` → fetch draft picks [1]
- `get_draft_traded_picks(draft_id)` → fetch traded picks [1]
- `get_sport_state(sport)` → fetch sport state [1]
- `get_players(sport, season)` → fetch player/projection-related payload used by the repository [1]
- `get_stats(sport, season_type, season)` → fetch season stats [1]
- `get_projections(sport, season_type, season, week)` → fetch weekly projections [1]

There are also references elsewhere to:
- `get_user(...)`
- `get_user_leagues(...)`
- `get_user_drafts(...)`
- `get_league(...)`
- `get_league_users(...)`
- `get_league_rosters(...)`

Those methods are required by the service layer, even though their full implementations were not included in the provided context [15][17][18].

---

## `BaseApi`

A very small helper that stores a shared API client. If no client is passed, it creates a `SleeperApiClient` automatically [2].

```python
from sleeper_wrapper import BaseApi

base = BaseApi()
print(base.client)
```

---

## Services

## `UserService`

`UserService` loads user-related data and returns model objects [18].

### Methods

#### `load_user(user_input, user_data=None) -> User`

Creates a `User` from provided data, or fetches it if `user_data` is missing [18].

```python
from sleeper_wrapper import UserService

service = UserService()
user = service.load_user("some_username")
print(user)
```

#### `get_all_leagues(user_id, season, sport) -> list[League]`

Fetches all leagues for a user and returns `League` objects [18].

```python
leagues = service.get_all_leagues(user_id=123456, season=2024, sport="nfl")
for league in leagues:
    print(league)
```

#### `get_all_drafts(user_id, season, sport) -> list[Draft]`

Fetches all drafts for a user and returns `Draft` objects [18].

```python
drafts = service.get_all_drafts(user_id=123456, season=2024, sport="nfl")
for draft in drafts:
    print(draft)
```

---

## `LeagueService`

`LeagueService` loads leagues and assembles their related objects [17].

### Methods

#### `load_league(league_id) -> League`

Fetches a league, builds a `League` model, and assembles related data [17].

```python
from sleeper_wrapper import LeagueService

league_service = LeagueService()
league = league_service.load_league(123456789)

print(league.league_name)
print(league.users)
print(league.teams)
print(league.drafts)
```

#### `get_week_matchups(league, week) -> list[Matchup]`

Loads matchup objects for a given week [17].

```python
matchups = league_service.get_week_matchups(league, 1)
for matchup in matchups:
    print(matchup.matchup_id, matchup.winning_roster_id)
```

#### `get_week_transactions(league, week) -> list[Transaction]`

Fetches and caches all transactions for a given week on the `league.transactions` dictionary [17].

```python
transactions = league_service.get_week_transactions(league, 1)
for tx in transactions:
    print(tx.transaction_id, tx.transaction_type)
```

#### `get_week_transactions_trades(league, week) -> list[Trade]`

Returns only trade transactions for a week [17].

```python
trades = league_service.get_week_transactions_trades(league, 1)
```

#### `get_week_transactions_waivers(league, week) -> list[Waiver]`

Returns only waiver transactions for a week [17].

```python
waivers = league_service.get_week_transactions_waivers(league, 1)
```

#### `get_week_transactions_free_agents(league, week) -> list[FreeAgent]`

Returns only free agent transactions for a week [17].

```python
free_agents = league_service.get_week_transactions_free_agents(league, 1)
```

---

## `DraftService`

`DraftService` loads draft-level data and constructs enriched pick objects [15].

### Methods

#### `load_draft(draft_id, draft_data=None) -> Draft`

Creates a `Draft` from provided data or fetches it if needed [15].

```python
from sleeper_wrapper import DraftService

draft_service = DraftService()
draft = draft_service.load_draft(123456789)

print(draft)
```

#### `get_all_picks(draft_id) -> list[Pick]`

Fetches all picks for a draft and enriches them with team/user lookups [15].

```python
picks = draft_service.get_all_picks(123456789)
for pick in picks:
    print(pick)
```

#### `get_all_traded_picks(draft_id) -> list[TradedPick]`

Fetches all traded picks for a draft [15].

```python
traded_picks = draft_service.get_all_traded_picks(123456789)
for traded_pick in traded_picks:
    print(traded_pick)
```

`DraftService` builds draft context by loading league users and rosters, then constructing lookup maps such as `users_by_id`, `teams_by_user_id`, and `teams_by_roster_id` [15].

---

## Models

## `User`

Represents a Sleeper user [12].

### Fields

- `user_id`
- `username`
- `display_name`
- `metadata` [12]

Example:

```python
from sleeper_wrapper import User

user = User("my_username", user_data=payload)
print(user.user_id)
print(user.display_name)
```

String form:

```python
print(user)
```

---

## `League`

Represents a Sleeper league [6].

### Core fields

- `league_id`
- `season`
- `sport`
- `settings`
- `scoring_settings`
- `first_week`
- `most_recent_week`
- `playoff_start`
- `num_teams`
- `league_status`
- `league_name`
- `roster_positions` [6]

### Assembled fields

The model also stores related data populated later:

- `users`
- `users_by_id`
- `teams`
- `teams_by_user_id`
- `teams_by_roster_id`
- `drafts`
- `all_players`
- `sport_state`
- `is_current_season`
- `transactions`
- `trades`
- `free_agents`
- `waiver`
- `matchups` [6]

Example:

```python
print(league.league_name)
print(league.num_teams)
```

---

## `Draft`

Represents a draft [5].

### Fields

- `draft_id`
- `season`
- `status`
- `settings`
- `metadata`
- `league_id`
- `sport`
- `draft_type`
- `slot_to_roster_id`
- `picks`
- `traded_picks`
- `teams` [5]

Example:

```python
from sleeper_wrapper import Draft

draft = Draft(123456789, draft_data=payload)
print(draft.draft_id)
print(draft.status)
```

---

## `Player`

Represents a Sleeper player [9].

### Fields

- `player_id`
- `first_name`
- `last_name`
- `full_name`
- `position`
- `stats` [9]

If name data is missing, `full_name` falls back to the `player_id` [9].

Example:

```python
from sleeper_wrapper import Player

player = Player("4046", player_data=payload)
print(player.full_name)
print(player.position)
```

---

## `Team`

Represents a league roster/team [10].

### Fields

- `roster_id`
- `user_obj`
- `team_name` [10]

Team name resolution:
1. If `user_obj` is missing, it becomes `Roster {roster_id}`
2. Otherwise it uses `user_obj.metadata["team_name"]` if present
3. Otherwise it uses `user_obj.display_name` [10]

Example:

```python
from sleeper_wrapper import Team

team = Team(roster_payload)
print(team.team_name)
```

---

## Matchup Models

The matchup layer includes:

- `Matchup`
- `MatchupTeam`
- `MatchupPlayer` [7]

### `Matchup`

A `Matchup` contains:
- `matchup_id`
- `teams`
- `winning_roster_id`
- `losing_roster_id`
- `winning_team`
- `losing_team` [7]

`Matchup.from_payload(...)` builds the object and determines the winner. If only one team exists in the matchup payload, that team is treated as the winner [7].

Example:

```python
for matchup in matchups:
    print(matchup.matchup_id)
    print(matchup.winning_roster_id)
```

`LeagueAssembler.assemble_week_matchups()` groups raw matchup entries by `matchup_id`, creates `Matchup` objects, attaches the corresponding `team_obj`, and enriches matchup players with full player objects [16].

---

## Draft Pick Models

## `Pick`

Represents a draft pick enriched with lookup context [8].

### Fields

- `pick_no`
- `round`
- `metadata`
- `player_id`
- `picked_by_user_id`
- `round_pick_number`
- `player_obj`
- `user_obj`
- `team_obj`
- `team_name` [8]

Example:

```python
for pick in picks:
    print(pick.pick_no, pick.player_id, pick.team_name)
```

## `TradedPick`

Represents a traded pick asset [8].

### Fields

- `season`
- `round`
- `original_roster_id`
- `previous_owner_roster_id`
- `current_owner_roster_id`
- `original_owner_team_obj`
- `previous_owner_team_obj`
- `current_owner_team_obj` [8]

---

## Transaction Models

The transaction model layer includes [11]:

- `Transaction`
- `Trade`
- `FreeAgent`
- `Waiver`
- `TransactionTeam`
- `TransactionPlayer`
- `TransactionPick`

### `TransactionPick`

Represents a pick moved in a transaction with:

- `round_number`
- `season`
- `old_roster_id`
- `new_roster_id` [11]

### `TransactionTeam`

Represents one team in a transaction with:

- `team_num`
- `roster_id`
- `team_obj`
- `user_obj`
- `players_added`
- `players_dropped` [11]

### Waiver-specific fields

`Waiver.from_payload(...)` adds:

- `added_player_ids`
- `dropped_player_ids`
- `waiver_bid`
- `waiver_seq`
- `message` [11]

`LeagueAssembler.assemble_week_transactions()` converts raw transaction payloads into `Trade`, `Waiver`, `FreeAgent`, or generic `Transaction` objects based on the payload type [16].

---

## Player Repository and Caching

## `FileCache`

A small JSON file cache helper for local storage [13].

### Methods

- `exists()`
- `read_json()`
- `write_json(data)`
- `read_or_none()` [13]

Example:

```python
from sleeper_wrapper import FileCache

cache = FileCache("players_nfl_2024.json")

if cache.exists():
    data = cache.read_json()
```

---

## `PlayerRepository`

Repository for loading players and returning `Player` objects, with optional local caching [14].

### Behavior

- Reuses in-memory player data if already loaded
- Otherwise tries local cache
- If cache is missing, fetches player data with `client.get_players(...)`
- Writes the fetched data to cache
- Normalizes the payload into a `player_id -> player_data` lookup [14]

Example:

```python
from sleeper_wrapper import SleeperApiClient, PlayerRepository

client = SleeperApiClient()
repo = PlayerRepository(client=client, sport="nfl", season=2024)

players_by_id = repo.load_players_by_id()
player = repo.get_player("4046")
print(player)
```

By default, cache files are named like:

```text
players_<sport>_<season>.json
```

Example:

```text
players_nfl_2024.json
```

[14]

---

## `AllPlayers`

A small wrapper around `PlayerRepository` for working with all players for a given sport/season [4].

### Fields

- `season`
- `sport`
- `client`
- `cache`
- `repository` [4]

### API

- `players_by_id` property
- `get_player(player_id)` [4]

Example:

```python
from sleeper_wrapper import AllPlayers

players = AllPlayers(season=2024, sport="nfl")
player = players.get_player("4046")
print(player)
```

---

## Common Usage Examples

### Load a user and their leagues

```python
from sleeper_wrapper import UserService

user_service = UserService()

user = user_service.load_user("some_username")
leagues = user_service.get_all_leagues(user.user_id, season=2024, sport="nfl")

print(user)
for league in leagues:
    print(league)
```

### Load a league and inspect teams

```python
from sleeper_wrapper import LeagueService

league_service = LeagueService()
league = league_service.load_league(123456789)

print(league)
for team in league.teams:
    print(team)
```

### Load weekly matchups

```python
from sleeper_wrapper import LeagueService

league_service = LeagueService()
league = league_service.load_league(123456789)

matchups = league_service.get_week_matchups(league, 1)

for matchup in matchups:
    print(f"Matchup {matchup.matchup_id}")
    print("Winner roster:", matchup.winning_roster_id)
```

### Load weekly transactions

```python
from sleeper_wrapper import LeagueService

league_service = LeagueService()
league = league_service.load_league(123456789)

transactions = league_service.get_week_transactions(league, 1)

for tx in transactions:
    print(tx)
```

### Load draft picks

```python
from sleeper_wrapper import DraftService

draft_service = DraftService()
picks = draft_service.get_all_picks(123456789)

for pick in picks:
    print(pick)
```

### Load traded picks

```python
from sleeper_wrapper import DraftService

draft_service = DraftService()
traded_picks = draft_service.get_all_traded_picks(123456789)

for traded_pick in traded_picks:
    print(traded_pick)
```

---

## Notes / Caveats

- Some client methods are referenced by the service layer but their full source was not included in the provided context, such as `get_user`, `get_user_leagues`, `get_user_drafts`, `get_league`, `get_league_users`, and `get_league_rosters` [15][17][18].
- The player-loading endpoint currently used by `get_players(sport, season)` points to a projections/root path rather than a classic Sleeper players endpoint, so you may want to verify whether that behavior is intentional for this repository [1].
- `LeagueService` creates `LeagueAssembler()` without passing its own client, so if you customize clients you may want to confirm shared client behavior in your local code [17].

---

## Minimal Example Script

```python
from sleeper_wrapper import UserService, LeagueService

user_service = UserService()
league_service = LeagueService()

user = user_service.load_user("some_username")
print(user)

leagues = user_service.get_all_leagues(user.user_id, season=2024, sport="nfl")
print(f"Found {len(leagues)} leagues")

if leagues:
    league = league_service.load_league(leagues[0].league_id)
    print(league.league_name)

    matchups = league_service.get_week_matchups(league, 1)
    for matchup in matchups:
        print(matchup.matchup_id, matchup.winning_roster_id)
```

---

## Suggested Future README Improvements

You may want to add:

- exact install instructions with `pyproject.toml` or `setup.py`
- supported Python versions
- complete `SleeperApiClient` method list
- error handling examples
- testing instructions
- examples for projections and stats endpoints [1]
```

If you want, I can also turn this into:
1. a cleaner `README.md`,
2. a shorter `docs/usage.md`, or
3. both files separated for direct copy/paste.
