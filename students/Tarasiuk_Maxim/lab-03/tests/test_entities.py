import pytest
from datetime import datetime
from src.domain.value_objects.ticker import Ticker
from src.domain.value_objects.quantity import Quantity
from src.domain.value_objects.money import Money
from src.domain.value_objects.transaction_type import TransactionType
from src.domain.entities.position import Position
from src.domain.entities.transaction import Transaction

def test_position_add_shares():
    pos = Position("pos1", Ticker("AAPL"))
    assert pos.id == "pos1"
    
    pos.add_shares(Quantity(10), Money(150.0, "USD"))
    assert pos.quantity.value == 10
    assert pos.average_price.amount == 150.0
    
    # Buy more at average 200
    pos.add_shares(Quantity(10), Money(200.0, "USD"))
    assert pos.quantity.value == 20
    assert pos.average_price.amount == 175.0

def test_position_remove_shares():
    pos = Position("pos1", Ticker("AAPL"))
    pos.add_shares(Quantity(20), Money(150.0, "USD"))
    
    pos.remove_shares(Quantity(5))
    assert pos.quantity.value == 15
    
    with pytest.raises(ValueError): # Try to remove too many
        pos.remove_shares(Quantity(30))

def test_transaction_equality():
    t1 = Transaction("t1", Ticker("AAPL"), TransactionType.BUY, Quantity(10), Money(100.0, "USD"), datetime.now())
    t2 = Transaction("t1", Ticker("AAPL"), TransactionType.BUY, Quantity(10), Money(100.0, "USD"), datetime.now())
    t3 = Transaction("t2", Ticker("AAPL"), TransactionType.BUY, Quantity(10), Money(100.0, "USD"), datetime.now())
    
    assert t1 == t2
    assert t1 != t3
    assert hash(t1) == hash(t2)
