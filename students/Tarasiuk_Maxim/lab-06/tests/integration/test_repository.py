import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.students.Tarasiuk_Maxim.lab_05.infrastructure.config.database import Base
from src.students.Tarasiuk_Maxim.lab_05.infrastructure.adapter.out.portfolio_repository import SqlAlchemyPortfolioRepository
from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio

# Using in-memory sqlite as requested by criteria flexibility/implementation choice
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    
@pytest.fixture
def repo(db_session):
    return SqlAlchemyPortfolioRepository(db_session)

def test_save_and_find_portfolio(repo):
    port = Portfolio("port_integration_1", "owner_123")
    port.add_transaction("AAPL", "BUY", 10, 150.0, "USD")
    
    # Act
    repo.save(port)
    
    # Reload from DB
    reloaded_port = repo.find_by_id("port_integration_1")
    
    # Assert
    assert reloaded_port is not None
    assert reloaded_port.id == "port_integration_1"
    assert reloaded_port.status == "ACTIVE"
    assert len(reloaded_port.positions()) == 1
    assert "AAPL" in reloaded_port._positions
    pos = list(reloaded_port.positions())[0]
    assert pos.quantity.value == 10

def test_find_all_active(repo):
    p1 = Portfolio("active_1", "owner1")
    p2 = Portfolio("active_2", "owner2")
    p3 = Portfolio("closed_1", "owner3")
    p3.close()
    
    repo.save(p1)
    repo.save(p2)
    repo.save(p3)
    
    active_ports = repo.find_all_active()
    ids = [p.id for p in active_ports]
    
    assert len(ids) == 2
    assert "active_1" in ids
    assert "active_2" in ids
    assert "closed_1" not in ids
