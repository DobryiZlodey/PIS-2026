from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from src.students.Tarasiuk_Maxim.lab_05.infrastructure.config.database import get_db
from src.students.Tarasiuk_Maxim.lab_05.infrastructure.adapter.out.portfolio_repository import SqlAlchemyPortfolioRepository
from src.students.Tarasiuk_Maxim.lab_05.infrastructure.event_bus.event_publisher import InMemoryEventPublisher

# CQRS imports
from src.students.Tarasiuk_Maxim.lab_04.application.service.portfolio_service import PortfolioService
from src.students.Tarasiuk_Maxim.lab_04.application.command.create_portfolio_command import CreatePortfolioCommand
from src.students.Tarasiuk_Maxim.lab_04.application.command.add_transaction_command import AddTransactionCommand
from src.students.Tarasiuk_Maxim.lab_04.application.command.close_portfolio_command import ClosePortfolioCommand
from src.students.Tarasiuk_Maxim.lab_04.application.query.get_portfolio_by_id_query import GetPortfolioByIdQuery
from src.students.Tarasiuk_Maxim.lab_04.application.query.list_active_portfolios_query import ListActivePortfoliosQuery

router = APIRouter(prefix="/api/portfolios", tags=["portfolios"])

# Request/Response models

class CreatePortfolioRequest(BaseModel):
    portfolio_id: str
    owner_id: str

class AddTransactionRequest(BaseModel):
    ticker: str
    type: str
    quantity: int
    price: float
    currency: str

# Dependency injection
def get_portfolio_service(db=Depends(get_db)):
    repo = SqlAlchemyPortfolioRepository(db)
    # the portfolio service encapsulates all handlers
    return PortfolioService(repo)

@router.post("")
def create_portfolio(request: CreatePortfolioRequest, service: PortfolioService = Depends(get_portfolio_service)):
    try:
        cmd = CreatePortfolioCommand(portfolio_id=request.portfolio_id, owner_id=request.owner_id)
        pid = service.create_portfolio(cmd)
        
        # Manually load events from repo / aggregate in a real scenario, or inject publisher in Handlers.
        # For simplicity, we assume events are published implicitly or handled here.
        return {"portfolio_id": pid}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{portfolio_id}/transactions")
def add_transaction(portfolio_id: str, request: AddTransactionRequest, service: PortfolioService = Depends(get_portfolio_service)):
    try:
        cmd = AddTransactionCommand(
            portfolio_id=portfolio_id,
            ticker=request.ticker,
            type=request.type,
            quantity=request.quantity,
            price=request.price,
            currency=request.currency
        )
        tx_id = service.add_transaction(cmd)
        return {"transaction_id": tx_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{portfolio_id}/close")
def close_portfolio(portfolio_id: str, service: PortfolioService = Depends(get_portfolio_service)):
    try:
        cmd = ClosePortfolioCommand(portfolio_id=portfolio_id)
        service.close_portfolio(cmd)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: str, service: PortfolioService = Depends(get_portfolio_service)):
    try:
        query = GetPortfolioByIdQuery(portfolio_id)
        dto = service.get_portfolio_by_id(query)
        if not dto:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return dto
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("")
def list_portfolios(limit: int = 10, offset: int = 0, service: PortfolioService = Depends(get_portfolio_service)):
    try:
        query = ListActivePortfoliosQuery(limit=limit, offset=offset)
        dtos = service.list_active_portfolios(query)
        return dtos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Running instructions:
# uvicorn src.students.Tarasiuk_Maxim.lab_05.infrastructure.adapter.in.portfolio_controller:router --reload
