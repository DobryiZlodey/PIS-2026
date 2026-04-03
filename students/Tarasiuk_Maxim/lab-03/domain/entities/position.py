from typing import Optional
from ..value_objects.ticker import Ticker
from ..value_objects.quantity import Quantity
from ..value_objects.money import Money

class Position:
    """Entity: Позиция по ценной бумаге в портфеле"""
    
    def __init__(self, position_id: str, ticker: Ticker):
        self._id = position_id
        self._ticker = ticker
        self._quantity = Quantity(1)  # Temporary init, usually managed by methods
        self._average_price = Money(0.0, "USD")
        self._is_empty = True
        
    @property
    def id(self) -> str:
        return self._id
        
    @property
    def ticker(self) -> Ticker:
        return self._ticker
        
    @property
    def quantity(self) -> Quantity:
        return self._quantity
        
    @property
    def average_price(self) -> Money:
        return self._average_price
        
    def add_shares(self, quantity: Quantity, price: Money) -> None:
        """Добавить акции к позиции (покупка)"""
        if self._is_empty:
            self._quantity = quantity
            self._average_price = price
            self._is_empty = False
        else:
            if self._average_price.currency != price.currency:
                raise ValueError("Currency mismatch")
            
            # Recalculate average price
            total_value_old = self._quantity.value * self._average_price.amount
            total_value_new = quantity.value * price.amount
            new_total_quantity = self._quantity.value + quantity.value
            new_avg_price = (total_value_old + total_value_new) / new_total_quantity
            
            self._quantity = Quantity(new_total_quantity)
            self._average_price = Money(new_avg_price, price.currency)
            
    def remove_shares(self, quantity: Quantity) -> None:
        """Удалить акции из позиции (продажа)"""
        if self._is_empty or self._quantity.value < quantity.value:
            raise ValueError(f"Not enough shares to remove. Have: {0 if self._is_empty else self._quantity.value}, requested: {quantity.value}")
            
        self._quantity = self._quantity.subtract(quantity.value)
        if self._quantity.value == 0:
            self._is_empty = True
            
    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self._id == other._id
        
    def __hash__(self):
        return hash(self._id)
