import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.students.Tarasiuk_Maxim.lab_05.infrastructure.config.database import Base, get_db
from src.students.Tarasiuk_Maxim.lab_05.infrastructure.adapter.in.portfolio_controller import router
from fastapi import FastAPI

# End-to-End setup mimicking the running application
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_full_portfolio_flow():
    # 1. Create a portfolio (POST /api/portfolios)
    resp_create = client.post(
        "/api/portfolios",
        json={"portfolio_id": "e2e_port", "owner_id": "e2e_owner"}
    )
    assert resp_create.status_code == 200
    assert resp_create.json()["portfolio_id"] == "e2e_port"
    
    # 2. Add transaction (POST /api/portfolios/{id}/transactions)
    resp_tx = client.post(
        "/api/portfolios/e2e_port/transactions",
        json={"ticker": "TSLA", "type": "BUY", "quantity": 5, "price": 200.0, "currency": "USD"}
    )
    assert resp_tx.status_code == 200
    assert "transaction_id" in resp_tx.json()
    
    # 3. Retrieve status (GET /api/portfolios/{id})
    resp_get = client.get("/api/portfolios/e2e_port")
    assert resp_get.status_code == 200
    data = resp_get.json()
    
    assert data["id"] == "e2e_port"
    assert data["status"] == "ACTIVE"
    assert len(data["positions"]) == 1
    assert data["positions"][0]["ticker"] == "TSLA"
    assert data["positions"][0]["quantity"] == 5
    
    # 4. Close portfolio (POST /api/portfolios/{id}/close)
    resp_close = client.post("/api/portfolios/e2e_port/close")
    assert resp_close.status_code == 200
    
    # 5. Verify it's closed
    resp_get2 = client.get("/api/portfolios/e2e_port")
    assert resp_get2.json()["status"] == "CLOSED"
    
    # 6. Cannot add transaction to closed portfolio
    resp_tx_fail = client.post(
        "/api/portfolios/e2e_port/transactions",
        json={"ticker": "TSLA", "type": "BUY", "quantity": 5, "price": 200.0, "currency": "USD"}
    )
    assert resp_tx_fail.status_code == 400
