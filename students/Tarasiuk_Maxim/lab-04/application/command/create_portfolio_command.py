from dataclasses import dataclass

@dataclass(frozen=True)
class CreatePortfolioCommand:
    """Command: Создать новый портфель инвестиций"""
    
    portfolio_id: str
    owner_id: str
    
    def __post_init__(self):
        if not self.portfolio_id or not isinstance(self.portfolio_id, str):
            raise ValueError("portfolio_id must be a non-empty string")
        if not self.owner_id or not isinstance(self.owner_id, str):
            raise ValueError("owner_id must be a non-empty string")
