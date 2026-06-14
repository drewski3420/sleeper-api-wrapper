from sleeper_wrapper import Draft

def test_get_specific_draft() -> None:
	draft = Draft(257270643320426496)
	specific_draft = draft.get_specific_draft()

	assert isinstance(specific_draft, dict)

def test_get_all_picks() -> None:
	draft = Draft(257270643320426496)
	all_picks = draft.get_all_picks()
	first_item = all_picks[0]

	assert isinstance(all_picks, list)
	assert isinstance(first_item, dict)

def test_get_traded_picks() -> None:
	draft = Draft(257270643320426496)
	traded_picks = draft.get_traded_picks()

	assert isinstance(traded_picks, list)
