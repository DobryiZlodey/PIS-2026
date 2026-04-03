from dataclasses import dataclass

@dataclass(frozen=True)
class Ticker:
    """Value Object: Биржевой тикер ценной бумаги"""
    
    symbol: str
    
    def __post_init__(self):
        if not self.symbol:
            raise ValueError("Ticker symbol cannot be empty")
        if not self.symbol.isupper():
            raise ValueError(f"Ticker symbol must be uppercase: {self.symbol}")
        if not (1 <= len(self.symbol) <= 5):
            raise ValueError(f"Ticker symbol length must be 1-5 chars: {self.symbol}")
        if not self.symbol.isalpha():
            raise ValueError(f"Ticker symbol must contain only letters: {self.symbol}")
