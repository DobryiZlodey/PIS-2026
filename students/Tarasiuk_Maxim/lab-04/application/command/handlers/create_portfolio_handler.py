from typing import Any
from src.students.Tarasiuk_Maxim.lab_04.application.port.out.portfolio_repository import PortfolioRepository
from ..create_portfolio_command import CreatePortfolioCommand

# Try to import domain
try:
    from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio
except ImportError:
    pass

class CreatePortfolioHandler:
    
    def __init__(self, repository):
        self.repository = repository
        
    def handle(self, command: CreatePortfolioCommand) -> str:
        # Create domain aggregate
        portfolio_id = command.portfolio_id
        owner_id = command.owner_id
        
        from src.students.Tarasiuk_Maxim.lab_03.domain.aggregates.portfolio import Portfolio
        portfolio = Portfolio(portfolio_id=portfolio_id, owner_id=owner_id)
        
        # Save to repository
        self.repository.save(portfolio)
        
        # Optionally, publish Domain Events here based on portfolio.events
        # event_bus.publish(portfolio.events)
        
        return portfolio.id
