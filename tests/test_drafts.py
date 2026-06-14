from sleeper_wrapper.all_players import AllPlayers
from sleeper_wrapper.base_api import BaseApi
from sleeper_wrapper.draft import Draft
from sleeper_wrapper.user import User
from sleeper_wrapper.team import Team


class FakeClient:
    def get_draft(self, draft_id: int) -> dict:
        return {
            "draft_id": draft_id,
            "last_picked": 1700000000000,
            "start_time": 1699990000000,
            "type": "snake",
            "metadata": {"scoring_type": "ppr"},
        }

    def get_draft_picks(self, draft_id: int) -> list:
        return [
            {
                "pick_no": 1,
                "round": 1,
                "picked_by": "101",
                "metadata": {
                    "player_id": "9001",
                    "first_name": "Josh",
                    "last_name": "Allen",
                    "position": "QB",
                },
            }
        ]

    def get_draft_traded_picks(self, draft_id: int) -> list:
        return []

    def get_players(self, sport: str) -> dict:
        return {
            "9001": {
                "first_name": "Josh",
                "last_name": "Allen",
                "position": "QB",
                "stats": {"adp_std": 1.0},
            }
        }

    def get_sport_state(self, sport: str) -> dict:
        return {"league_season": "2024"}


def setup_function() -> None:
    BaseApi.set_client(FakeClient())
    AllPlayers._cache = {}


def _build_draft() -> Draft:
    user = User(
        101,
        user_data={
            "user_id": "101",
            "username": "alpha",
            "display_name": "Alpha",
            "metadata": {"team_name": "Alpha Team"},
        },
    )
    team = Team({"roster_id": "1", "owner_id": "101", "user": user})

    return Draft(
        257270643320426496,
        users_by_id={101: user},
        teams_by_user_id={101: team},
    )


def test_get_specific_draft() -> None:
    draft = _build_draft()

    assert isinstance(draft, Draft)
    assert draft.draft_id == 257270643320426496
    assert draft.type == "snake"


def test_get_all_picks() -> None:
    draft = _build_draft()
    all_picks = draft.picks
    first_item = all_picks[0]

    assert isinstance(all_picks, list)
    assert first_item.pick_no == 1
    assert first_item.player.full_name == "Josh Allen"


def test_get_traded_picks() -> None:
    draft = _build_draft()
    traded_picks = draft.traded_picks

    assert isinstance(traded_picks, list)
    assert traded_picks == []
