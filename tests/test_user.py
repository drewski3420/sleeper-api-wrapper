from sleeper_wrapper import User

def test_get_user() -> None:
	user = User("blah")
	user = user.get_user()
	assert isinstance(user, dict)
	assert user['username'] == "blah"

def test_get_all_leagues() -> None:
	user = User("drewski3420")
	leagues = user.get_all_leagues("nfl", 2025)

	assert isinstance(leagues, list)
	assert isinstance(leagues[0], dict)

	user = User("swa")
	leagues = user.get_all_leagues("nfl", 2025)
	assert isinstance(leagues, list)
	assert isinstance(leagues[0], dict)

def test_get_all_drafts() -> None:
	user = User("swa")
	drafts = user.get_all_drafts("nfl", 2025)
	assert isinstance(drafts, list)
	assert isinstance(drafts[0], dict)
