import pytest
from src.domain.aggregates.portfolio import Portfolio

def test_domain_events_registered():
    p = Portfolio("p1", "u1")
    
    p.clear_events()
    assert len(p.events) == 0
    
    p.add_transaction("AAPL", "BUY", 5, 100.0, "USD")
    events = p.events
    assert len(events) == 1
    assert events[0].__class__.__name__ == "TransactionAddedEvent"
    assert events[0].ticker_symbol == "AAPL"
    
    p.clear_events()
    p.close()
    
    events = p.events
    assert len(events) == 1
    assert events[0].__class__.__name__ == "PortfolioClosedEvent"
