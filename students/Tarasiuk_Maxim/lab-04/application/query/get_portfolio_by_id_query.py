from dataclasses import dataclass

@dataclass(frozen=True)
class GetPortfolioByIdQuery:
    """Query: Получить портфель по его ID"""
    portfolio_id: str
    
    def __post_init__(self):
        if not self.portfolio_id:
            raise ValueError("portfolio_id cannot be empty")
