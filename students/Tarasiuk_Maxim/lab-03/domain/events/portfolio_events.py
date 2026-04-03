from datetime import datetime
from dataclasses import dataclass, field
from src.domain.events.domain_event import DomainEvent
try:
    from ...value_objects.money import Money
    from ...value_objects.ticker import Ticker
    from ...value_objects.quantity import Quantity
    from ...value_objects.transaction_type import TransactionType
except ImportError:
    # Handles direct running
    pass

@dataclass
class PortfolioCreatedEvent(DomainEvent):
    portfolio_id: str
    owner_id: str
    _occurred_on: datetime = field(default_factory=datetime.now)

    def occurred_on(self) -> datetime:
        return self._occurred_on

@dataclass
class TransactionAddedEvent(DomainEvent):
    portfolio_id: str
    transaction_id: str
    ticker_symbol: str
    type_name: str
    quantity_value: int
    price_amount: float
    _occurred_on: datetime = field(default_factory=datetime.now)

    def occurred_on(self) -> datetime:
        return self._occurred_on

@dataclass
class PortfolioClosedEvent(DomainEvent):
    portfolio_id: str
    _occurred_on: datetime = field(default_factory=datetime.now)

    def occurred_on(self) -> datetime:
        return self._occurred_on
