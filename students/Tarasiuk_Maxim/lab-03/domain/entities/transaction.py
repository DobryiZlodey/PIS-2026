from datetime import datetime
from ..value_objects.ticker import Ticker
from ..value_objects.quantity import Quantity
from ..value_objects.money import Money
from ..value_objects.transaction_type import TransactionType

class Transaction:
    """Entity: Сделка (история операций)"""
    
    def __init__(self, transaction_id: str, ticker: Ticker, type_: TransactionType, 
                 quantity: Quantity, price: Money, date: datetime):
        self._id = transaction_id
        self._ticker = ticker
        self._type = type_
        self._quantity = quantity
        self._price = price
        self._date = date
        
        # Инвариант создания транзакции
        if not isinstance(ticker, Ticker):
            raise ValueError()
        if not isinstance(quantity, Quantity):
            raise ValueError()
        if not isinstance(price, Money):
            raise ValueError()
            
    @property
    def id(self) -> str:
        return self._id
        
    @property
    def ticker(self) -> Ticker:
        return self._ticker
        
    @property
    def type(self) -> TransactionType:
        return self._type
        
    @property
    def quantity(self) -> Quantity:
        return self._quantity
        
    @property
    def price(self) -> Money:
        return self._price
        
    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return False
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)
