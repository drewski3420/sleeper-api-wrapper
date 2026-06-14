import pytest


@pytest.mark.skip(
    reason="Legacy trending players test targets an older Player API. "
    "Add the current player/trending implementation files to the chat to update this test."
)
def test_get_trending_players() -> None:
    pass
