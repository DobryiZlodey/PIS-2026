from dataclasses import dataclass

@dataclass(frozen=True)
class ListActivePortfoliosQuery:
    """Query: Получить все активные портфели (с пагинацией)"""
    limit: int = 10
    offset: int = 0
    
    def __post_init__(self):
        if self.limit <= 0:
            raise ValueError("Limit must be positive")
        if self.offset < 0:
            raise ValueError("Offset cannot be negative")
