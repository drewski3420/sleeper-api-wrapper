import pytest
from datetime import datetime
from unittest.mock import Mock, patch

#from test_classes import *
from sleeper_wrapper.models.transaction import Transaction
from fixtures import TEST_LEAGUE_SCENARIO

#LEAGUE_ID = TEST_LEAGUE_SCENARIO['league_id']
#USER_ID = TEST_LEAGUE_SCENARIO['users'][0]['user_id']
#DRAFT_ID = TEST_LEAGUE_SCENARIO['drafts'][0]['draft_id']
#SPORT = TEST_LEAGUE_SCENARIO['sport']
#YEAR = TEST_LEAGUE_SCENARIO['sport_state']['season']
#WEEK = TEST_LEAGUE_SCENARIO['sport_state']['week']
TRANSACTION = TEST_LEAGUE_SCENARIO['transactions'][0]

transaction = Transaction.from_payload(TRANSACTION)

def test_transaction_initializes_with_full_payload():
  assert transaction.transaction_id == int(TRANSACTION['transaction_id'])
  assert transaction.status == TRANSACTION['status']
  assert transaction.status_updated == datetime.fromtimestamp(TRANSACTION['status_updated'] / 1000)
  assert transaction.creator == TRANSACTION['creator']
  assert transaction.created == datetime.fromtimestamp(TRANSACTION['created'] / 1000)
  assert len(transaction.teams) == len(TRANSACTION['roster_ids'])
  assert transaction.adds == TRANSACTION['adds']
  assert transaction.drops == TRANSACTION['drops']

def test_transaction_owners_are_parsed_correctly():
  print(transaction.teams[0].__dict__) #team_obj.team_name == "feiyingx"
#def test_transaction_status_fields():
#def test_transaction_str_representation():
#def test_transaction_from_dict_or_factory_if_present():


if __name__=='__main__':
#  test_transaction_initializes_with_full_payload()
  test_transaction_owners_are_parsed_correctly()
