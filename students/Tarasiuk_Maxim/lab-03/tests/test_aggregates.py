import pytest
from src.domain.aggregates.portfolio import Portfolio

def test_portfolio_creation():
    p = Portfolio("port1", "user1")
    assert p.id == "port1"
    assert p.status == "ACTIVE"
    events = p.events
    assert len(events) == 1
    assert events[0].__class__.__name__ == "PortfolioCreatedEvent"

def test_add_transaction_buy():
    p = Portfolio("port1", "user1")
    tx_id = p.add_transaction("AAPL", "BUY", 10, 150.0, "USD")
    
    assert tx_id is not None
    assert len(p.positions()) == 1
    
    pos = p.positions()[0]
    assert pos.ticker.symbol == "AAPL"
    assert pos.quantity.value == 10
    assert pos.average_price.amount == 150.0

def test_sell_invariant():
    p = Portfolio("port1", "user1")
    p.add_transaction("AAPL", "BUY", 10, 150.0, "USD")
    
    # valid sell
    p.add_transaction("AAPL", "SELL", 4, 160.0, "USD")
    pos = p.positions()[0]
    assert pos.quantity.value == 6
    
    # invalid sell - over requested amount
    with pytest.raises(ValueError):
        p.add_transaction("AAPL", "SELL", 10, 160.0, "USD")
        
    # invalid sell - non existent position
    with pytest.raises(ValueError):
        p.add_transaction("MSFT", "SELL", 5, 200.0, "USD")

def test_portfolio_closed_invariant():
    p = Portfolio("port1", "user1")
    p.close()
    
    assert p.status == "CLOSED"
    
    with pytest.raises(ValueError):
        p.add_transaction("AAPL", "BUY", 10, 150.0, "USD")
        
    with pytest.raises(ValueError):
        p.close()
