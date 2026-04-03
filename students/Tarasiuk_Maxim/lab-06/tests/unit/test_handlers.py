import pytest
from unittest.mock import Mock

from src.students.Tarasiuk_Maxim.lab_04.application.command.create_portfolio_command import CreatePortfolioCommand
from src.students.Tarasiuk_Maxim.lab_04.application.command.handlers.create_portfolio_handler import CreatePortfolioHandler
from src.students.Tarasiuk_Maxim.lab_04.application.command.add_transaction_command import AddTransactionCommand
from src.students.Tarasiuk_Maxim.lab_04.application.command.handlers.add_transaction_handler import AddTransactionHandler
from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio

def test_create_portfolio_handler():
    # Arrange 
    mock_repo = Mock()
    handler = CreatePortfolioHandler(mock_repo)
    command = CreatePortfolioCommand("port123", "owner123")
    
    # Act
    handler.handle(command)
    
    # Assert
    mock_repo.save.assert_called_once()
    saved_entity = mock_repo.save.call_args[0][0]
    assert isinstance(saved_entity, Portfolio)
    assert saved_entity.id == "port123"

def test_add_transaction_handler():
    # Arrange
    mock_repo = Mock()
    handler = AddTransactionHandler(mock_repo)
    
    dummy_portfolio = Portfolio("port123", "owner123")
    mock_repo.find_by_id.return_value = dummy_portfolio
    
    command = AddTransactionCommand("port123", "MSFT", "BUY", 5, 200.0, "USD")
    
    # Act
    handler.handle(command)
    
    # Assert
    mock_repo.find_by_id.assert_called_once_with("port123")
    mock_repo.save.assert_called_once_with(dummy_portfolio)
    assert len(dummy_portfolio.positions()) == 1
    
    pos = list(dummy_portfolio.positions())[0]
    assert pos.ticker.symbol == "MSFT"

def test_add_transaction_portfolio_not_found():
    mock_repo = Mock()
    handler = AddTransactionHandler(mock_repo)
    mock_repo.find_by_id.return_value = None
    
    command = AddTransactionCommand("port123", "MSFT", "BUY", 5, 200.0, "USD")
    
    with pytest.raises(ValueError, match="not found"):
        handler.handle(command)
