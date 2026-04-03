import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.students.Tarasiuk_Maxim.lab_05.infrastructure.config.database import Base, get_db
from src.students.Tarasiuk_Maxim.lab_05.infrastructure.adapter.in.portfolio_controller import router
from fastapi import FastAPI

# Setup in-memory DB for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_portfolio():
    response = client.post(
        "/api/portfolios",
        json={"portfolio_id": "test_port", "owner_id": "owner_1"}
    )
    assert response.status_code == 200
    assert response.json() == {"portfolio_id": "test_port"}

def test_get_portfolio():
    # Setup state
    client.post("/api/portfolios", json={"portfolio_id": "port2", "owner_id": "owner2"})
    
    response = client.get("/api/portfolios/port2")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "port2"
    assert data["owner_id"] == "owner2"

def test_add_transaction():
    client.post("/api/portfolios", json={"portfolio_id": "port3", "owner_id": "owner3"})
    
    response = client.post(
        "/api/portfolios/port3/transactions",
        json={
            "ticker": "AAPL",
            "type": "BUY",
            "quantity": 10,
            "price": 150.0,
            "currency": "USD"
        }
    )
    assert response.status_code == 200
    assert "transaction_id" in response.json()
    
def test_list_portfolios():
    response = client.get("/api/portfolios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
