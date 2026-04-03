import pytest
from unittest.mock import Mock

from src.students.Tarasiuk_Maxim.lab_04.application.query.get_portfolio_by_id_query import GetPortfolioByIdQuery
from src.students.Tarasiuk_Maxim.lab_04.application.query.handlers.get_portfolio_by_id_handler import GetPortfolioByIdHandler
from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio

def test_get_portfolio_by_id_handler():
    repo_mock = Mock()
    handler = GetPortfolioByIdHandler(repo_mock)
    
    p = Portfolio("port1", "owner1")
    p.add_transaction("AAPL", "BUY", 5, 100.0, "USD")
    repo_mock.find_by_id.return_value = p
    
    query = GetPortfolioByIdQuery("port1")
    dto = handler.handle(query)
    
    assert dto is not None
    assert dto.id == "port1"
    assert len(dto.positions) == 1
    assert dto.positions[0].ticker == "AAPL"
    assert dto.positions[0].quantity == 5
    
    assert len(dto.transactions) == 1
    assert dto.transactions[0].type_name == "BUY"

def test_get_portfolio_by_id_not_found():
    repo_mock = Mock()
    handler = GetPortfolioByIdHandler(repo_mock)
    
    repo_mock.find_by_id.return_value = None
    query = GetPortfolioByIdQuery("invalid_id")
    dto = handler.handle(query)
    
    assert dto is None
