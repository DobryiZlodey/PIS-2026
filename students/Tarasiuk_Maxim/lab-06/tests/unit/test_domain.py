import pytest
from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio
from src.students.Tarasiuk_Maxim.lab_03.domain.value_objects.ticker import Ticker
from src.students.Tarasiuk_Maxim.lab_03.domain.value_objects.quantity import Quantity
from src.students.Tarasiuk_Maxim.lab_03.domain.value_objects.money import Money

def test_portfolio_initialization():
    portfolio = Portfolio("port1", "owner1")
    assert portfolio.id == "port1"
    assert portfolio.status == "ACTIVE"
    # Event should be published
    assert any(e.__class__.__name__ == "PortfolioCreatedEvent" for e in portfolio.events)

def test_add_transaction_success():
    portfolio = Portfolio("port1", "owner1")
    portfolio.clear_events()
    
    tx_id = portfolio.add_transaction("AAPL", "BUY", 10, 150.0, "USD")
    
    # Assert state mutation
    assert tx_id is not None
    assert len(portfolio.positions()) == 1
    pos = list(portfolio.positions())[0]
    
    assert pos.ticker.symbol == "AAPL"
    assert pos.quantity.value == 10
    assert pos.average_price.amount == 150.0
    
    # Assert Events are emitted
    assert any(e.__class__.__name__ == "TransactionAddedEvent" for e in portfolio.events)

def test_sell_transaction_invalid_quantity():
    portfolio = Portfolio("port1", "owner1")
    portfolio.add_transaction("AAPL", "BUY", 5, 100.0, "USD")
    
    with pytest.raises(ValueError, match="Not enough quantity to sell"):
        portfolio.add_transaction("AAPL", "SELL", 10, 100.0, "USD")

def test_close_portfolio():
    portfolio = Portfolio("port1", "owner1")
    portfolio.close()
    
    assert portfolio.status == "CLOSED"
    assert any(e.__class__.__name__ == "PortfolioClosedEvent" for e in portfolio.events)

    with pytest.raises(ValueError, match="Cannot add transaction to a non-active portfolio"):
        portfolio.add_transaction("AAPL", "BUY", 5, 100.0, "USD")
