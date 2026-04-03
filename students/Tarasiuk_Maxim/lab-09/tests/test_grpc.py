import pytest
from unittest.mock import MagicMock
import grpc

# Using the simulated modules from our server architecture
from src.students.Tarasiuk_Maxim.lab_09.grpc.server import PortfolioServicer

class MockContext:
    def __init__(self):
        self.code = None
        self.details = None
        
    def set_code(self, code):
        self.code = code
        
    def set_details(self, details):
        self.details = details

class MockCreateRequest:
    def __init__(self, portfolio_id, owner_id):
        self.portfolio_id = portfolio_id
        self.owner_id = owner_id

class MockGetRequest:
    def __init__(self, portfolio_id):
        self.portfolio_id = portfolio_id

def test_create_portfolio_grpc():
    servicer = PortfolioServicer()
    context = MockContext()
    
    # Create success
    req = MockCreateRequest("port200", "owner200")
    resp = servicer.CreatePortfolio(req, context)
    
    assert resp.portfolio_id == "port200"
    assert resp.status == "CREATED"
    
    # Create already exists
    resp_dup = servicer.CreatePortfolio(req, context)
    assert context.code == grpc.StatusCode.ALREADY_EXISTS

def test_get_portfolio_grpc():
    servicer = PortfolioServicer()
    context = MockContext()
    
    # Requesting non-existent
    req = MockGetRequest("unknown")
    resp = servicer.GetPortfolio(req, context)
    assert context.code == grpc.StatusCode.NOT_FOUND
    assert resp.status == "NOT_FOUND"
    
    # Requesting valid
    req2 = MockGetRequest("port1") # "port1" is preloaded in constructor
    resp2 = servicer.GetPortfolio(req2, context)
    assert resp2.portfolio_id == "port1"

def test_stream_active_portfolios():
    servicer = PortfolioServicer()
    context = MockContext()
    
    stream_generator = servicer.StreamActivePortfolios(None, context)
    responses = list(stream_generator)
    
    assert len(responses) == 1
    assert responses[0].portfolio_id == "port1"
