from __future__ import annotations

import json
from pathlib import Path

import pytest

from sleeper_wrapper import User


def _load_test_config() -> dict:
    config_path = Path(__file__).resolve().parent / "local_test_config.json"
    if not config_path.exists():
        pytest.skip(
            "Missing tests/local_test_config.json. Copy tests/local_test_config.example.json "
            "to tests/local_test_config.json and fill in your local values."
        )

    with config_path.open(encoding="utf-8") as config_file:
        return json.load(config_file)


def _get_username(key: str) -> str:
    config = _load_test_config()
    username = config.get(key)
    if not username:
        pytest.skip(f"Missing '{key}' in tests/local_test_config.json")
    return username


def test_get_user() -> None:
    username = _get_username("primary_username")
    user = User(username)
    user = user.get_user()
    assert isinstance(user, dict)
    assert user["username"] == username


def test_get_all_leagues() -> None:
    username = _get_username("primary_username")
    user = User(username)
    leagues = user.get_all_leagues("nfl", 2025)

    assert isinstance(leagues, list)
    assert isinstance(leagues[0], dict)

    secondary_username = _get_username("secondary_username")
    user = User(secondary_username)
    leagues = user.get_all_leagues("nfl", 2025)
    assert isinstance(leagues, list)
    assert isinstance(leagues[0], dict)


def test_get_all_drafts() -> None:
    username = _get_username("secondary_username")
    user = User(username)
    drafts = user.get_all_drafts("nfl", 2025)
    assert isinstance(drafts, list)
    assert isinstance(drafts[0], dict)
