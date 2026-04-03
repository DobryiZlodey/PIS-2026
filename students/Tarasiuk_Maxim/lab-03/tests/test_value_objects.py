import pytest
from src.domain.value_objects.money import Money
from src.domain.value_objects.ticker import Ticker
from src.domain.value_objects.quantity import Quantity
from src.domain.value_objects.transaction_type import TransactionType

def test_money_creation():
    m = Money(100.5, "USD")
    assert m.amount == 100.5
    assert m.currency == "USD"

def test_money_validation():
    with pytest.raises(ValueError):
        Money(-10, "USD")
    with pytest.raises(ValueError):
        Money(10, "US")

def test_money_addition():
    m1 = Money(10.0, "USD")
    m2 = Money(5.5, "USD")
    assert (m1 + m2).amount == 15.5

def test_money_subtraction():
    m1 = Money(10.0, "USD")
    m2 = Money(3.0, "USD")
    assert (m1 - m2).amount == 7.0

def test_money_substraction_fails_if_negative():
    m1 = Money(10.0, "USD")
    m2 = Money(15.0, "USD")
    with pytest.raises(ValueError):
        m1 - m2

def test_ticker_validation():
    with pytest.raises(ValueError):
        Ticker("aapl")
    with pytest.raises(ValueError):
        Ticker("A1")
    with pytest.raises(ValueError):
        Ticker("TOOLONG")
    
    t = Ticker("AAPL")
    assert t.symbol == "AAPL"

def test_quantity():
    q = Quantity(10)
    assert q.value == 10
    
    with pytest.raises(ValueError):
        Quantity(0)
    with pytest.raises(ValueError):
        Quantity(-5)
        
def test_transaction_type():
    assert TransactionType.BUY.value == "BUY"
    assert TransactionType.SELL.value == "SELL"
    with pytest.raises(ValueError):
        TransactionType("HOLD")
