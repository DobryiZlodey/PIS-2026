from dataclasses import dataclass

@dataclass(frozen=True)
class ClosePortfolioCommand:
    """Command: Закрыть портфель инвестиций"""
    
    portfolio_id: str
    
    def __post_init__(self):
        if not self.portfolio_id or not isinstance(self.portfolio_id, str):
            raise ValueError("portfolio_id must be a non-empty string")
