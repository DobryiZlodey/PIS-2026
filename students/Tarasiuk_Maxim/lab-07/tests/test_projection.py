import pytest
import json
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.students.Tarasiuk_Maxim.lab_05.infrastructure.config.database import Base
from src.students.Tarasiuk_Maxim.lab_07.cqrs.read_model.portfolio_view import PortfolioViewOrm
from src.students.Tarasiuk_Maxim.lab_07.cqrs.projection.portfolio_projection import PortfolioProjectionHandler

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@dataclass
class DummyCreatedEvent:
    portfolio_id: str
    owner_id: str
    timestamp: datetime

@dataclass
class DummyTxAddedEvent:
    portfolio_id: str
    tx_id: str
    ticker: str
    type: str
    quantity: int
    price: float
    currency: str
    timestamp: datetime

@dataclass
class DummyClosedEvent:
    portfolio_id: str
    timestamp: datetime

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def test_sync_projection(db_session):
    handler = PortfolioProjectionHandler(db_session)
    
    # 1. Fire Portfolio Created Event
    ev1 = DummyCreatedEvent("port123", "owner123", datetime.now())
    handler.handle_portfolio_created(ev1)
    
    view = db_session.query(PortfolioViewOrm).filter_by(portfolio_id="port123").first()
    assert view is not None
    assert view.status == "ACTIVE"
    data = json.loads(view.view_data)
    assert len(data["positions"]) == 0
    assert len(data["transactions"]) == 0
    
    # 2. Fire Transaction Added Event
    ev2 = DummyTxAddedEvent("port123", "tx1", "AAPL", "BUY", 10, 150.0, "USD", datetime.now())
    handler.handle_transaction_added(ev2)
    
    view = db_session.query(PortfolioViewOrm).filter_by(portfolio_id="port123").first()
    data = json.loads(view.view_data)
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["ticker"] == "AAPL"
    assert len(data["positions"]) == 1
    assert data["positions"][0]["quantity"] == 10
    
    # Fire another buy
    ev3 = DummyTxAddedEvent("port123", "tx2", "AAPL", "BUY", 5, 160.0, "USD", datetime.now())
    handler.handle_transaction_added(ev3)
    view = db_session.query(PortfolioViewOrm).filter_by(portfolio_id="port123").first()
    data = json.loads(view.view_data)
    assert len(data["positions"]) == 1
    assert data["positions"][0]["quantity"] == 15
    
    # 3. Fire Closed Event
    ev4 = DummyClosedEvent("port123", datetime.now())
    handler.handle_portfolio_closed(ev4)
    
    view = db_session.query(PortfolioViewOrm).filter_by(portfolio_id="port123").first()
    assert view.status == "CLOSED"
