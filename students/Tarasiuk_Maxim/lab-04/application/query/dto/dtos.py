from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class PositionDto:
    ticker: str
    quantity: int
    average_price: float
    currency: str

@dataclass(frozen=True)
class TransactionDto:
    id: str
    ticker: str
    type_name: str
    quantity: int
    price: float
    currency: str
    date_iso: str

@dataclass(frozen=True)
class PortfolioDto:
    id: str
    owner_id: str
    status: str
    positions: List[PositionDto] = field(default_factory=list)
    transactions: List[TransactionDto] = field(default_factory=list)
