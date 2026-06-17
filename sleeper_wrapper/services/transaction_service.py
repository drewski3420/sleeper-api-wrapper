"""Transaction-related service operations."""

from __future__ import annotations

from ..api_client import SleeperApiClient
from ..models.transaction import FreeAgent, Trade, Transaction, Waiver


class TransactionService:
  """Load and classify transactions from the API."""

  def __init__(self, client: SleeperApiClient | None = None) -> None:
    self.client = client or SleeperApiClient()

  def load_week_transactions(self, league_id: int, week: int) -> list[Transaction]:
    raw_transactions = self.client.get_week_transactions(league_id, week)
    transactions: list[Transaction] = []

    for data in raw_transactions:
      tx_type = data.get("type")
      if tx_type == "trade":
        transactions.append(Trade.from_payload(data))
      elif tx_type == "free_agent":
        transactions.append(FreeAgent.from_payload(data))
      elif tx_type == "waiver":
        transactions.append(Waiver.from_payload(data))
      else:
        transactions.append(Transaction.from_payload(data))

    return transactions
