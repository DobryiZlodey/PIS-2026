from ..close_portfolio_command import ClosePortfolioCommand

class ClosePortfolioHandler:
    
    def __init__(self, repository):
        self.repository = repository
        
    def handle(self, command: ClosePortfolioCommand) -> None:
        portfolio = self.repository.find_by_id(command.portfolio_id)
        if not portfolio:
            raise ValueError(f"Portfolio {command.portfolio_id} not found")
            
        portfolio.close()
        
        self.repository.save(portfolio)
