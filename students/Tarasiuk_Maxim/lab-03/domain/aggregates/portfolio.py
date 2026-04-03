from typing import List, Optional
from datetime import datetime
import uuid

from ..entities.position import Position
from ..entities.transaction import Transaction
from ..value_objects.ticker import Ticker
from ..value_objects.quantity import Quantity
from ..value_objects.money import Money
from ..value_objects.transaction_type import TransactionType
from ..events.domain_event import DomainEvent
from ..events.portfolio_events import (
    PortfolioCreatedEvent, 
    TransactionAddedEvent, 
    PortfolioClosedEvent
)

class Portfolio:
    """Aggregate Root: Портфель инвестора"""
    
    def __init__(self, portfolio_id: str, owner_id: str):
        if not portfolio_id or not owner_id:
            raise ValueError("ID and owner_id are required")
            
        self._id = portfolio_id
        self._owner_id = owner_id
        self._status = "ACTIVE"
        
        self._positions = {}  # dict of ticker_symbol -> Position
        self._transactions: List[Transaction] = []
        
        self._events: List[DomainEvent] = []
        
        self._events.append(PortfolioCreatedEvent(
            portfolio_id=self._id, 
            owner_id=self._owner_id
        ))
        
    @property
    def id(self) -> str:
        return self._id
        
    @property
    def status(self) -> str:
        return self._status
        
    @property
    def events(self) -> List[DomainEvent]:
        return list(self._events)
        
    def clear_events(self) -> None:
        self._events.clear()
        
    def positions(self) -> List[Position]:
        return list(self._positions.values())
        
    def add_transaction(self, ticker_str: str, type_name: str, quantity_val: int, price_val: float, currency: str) -> str:
        """Регистрирует транзакцию купли-продажи (инварианты проверяются)"""
        
        if self._status != "ACTIVE":
            raise ValueError("Cannot add transaction to a non-active portfolio")
            
        ticker = Ticker(ticker_str)
        quantity = Quantity(quantity_val)
        price = Money(price_val, currency)
        
        trx_type = TransactionType(type_name)
        
        # Invariant checks for SELL
        if trx_type == TransactionType.SELL:
            if ticker.symbol not in self._positions:
                raise ValueError(f"Cannot sell {ticker.symbol}: position does not exist")
                
            pos = self._positions[ticker.symbol]
            if pos.quantity.value < quantity.value:
                raise ValueError(f"Cannot sell {quantity.value} of {ticker.symbol}: only {pos.quantity.value} available")
                
        # Business logic: update position
        if ticker.symbol not in self._positions:
            self._positions[ticker.symbol] = Position(f"POS-{self._id}-{ticker.symbol}", ticker)
            
        position = self._positions[ticker.symbol]
        
        if trx_type == TransactionType.BUY:
            position.add_shares(quantity, price)
        elif trx_type == TransactionType.SELL:
            position.remove_shares(quantity)
            
        # Create transaction record
        tx_id = str(uuid.uuid4())
        txn = Transaction(tx_id, ticker, trx_type, quantity, price, datetime.now())
        self._transactions.append(txn)
        
        self._events.append(TransactionAddedEvent(
            portfolio_id=self._id,
            transaction_id=tx_id,
            ticker_symbol=ticker.symbol,
            type_name=trx_type.value,
            quantity_value=quantity.value,
            price_amount=price.amount
        ))
        
        return tx_id
        
    def close(self) -> None:
        if self._status == "CLOSED":
            raise ValueError("Portfolio is already closed")
            
        self._status = "CLOSED"
        self._events.append(PortfolioClosedEvent(portfolio_id=self._id))
