import pytest
from unittest.mock import Mock, MagicMock
import sys

from src.students.Tarasiuk_Maxim.lab_04.application.command.create_portfolio_command import CreatePortfolioCommand
from src.students.Tarasiuk_Maxim.lab_04.application.command.handlers.create_portfolio_handler import CreatePortfolioHandler
from src.students.Tarasiuk_Maxim.lab_04.application.command.add_transaction_command import AddTransactionCommand
from src.students.Tarasiuk_Maxim.lab_04.application.command.handlers.add_transaction_handler import AddTransactionHandler

from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio

def test_create_portfolio_handler():
    repo_mock = Mock()
    handler = CreatePortfolioHandler(repo_mock)
    
    cmd = CreatePortfolioCommand("port1", "owner1")
    res_id = handler.handle(cmd)
    
    assert res_id == "port1"
    repo_mock.save.assert_called_once()
    saved_arg = repo_mock.save.call_args[0][0]
    assert isinstance(saved_arg, Portfolio)
    assert len(saved_arg.events) > 0  # PortfolioCreatedEvent

def test_add_transaction_handler():
    repo_mock = Mock()
    handler = AddTransactionHandler(repo_mock)
    
    # Mock existing portfolio
    portfolio = Portfolio("port1", "owner1")
    repo_mock.find_by_id.return_value = portfolio
    
    cmd = AddTransactionCommand("port1", "AAPL", "BUY", 10, 150.0, "USD")
    tx_id = handler.handle(cmd)
    
    assert tx_id is not None
    repo_mock.find_by_id.assert_called_with("port1")
    repo_mock.save.assert_called_with(portfolio)
    assert len(portfolio.positions()) == 1
    
    events = portfolio.events
    assert any(e.__class__.__name__ == "TransactionAddedEvent" for e in events)
