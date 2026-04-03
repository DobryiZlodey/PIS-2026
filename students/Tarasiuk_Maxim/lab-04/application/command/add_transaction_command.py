from dataclasses import dataclass

@dataclass(frozen=True)
class AddTransactionCommand:
    """Command: Добавить сделку (покупка/продажа) в портфель"""
    
    portfolio_id: str
    ticker: str
    type: str # "BUY" or "SELL"
    quantity: int
    price: float
    currency: str
    
    def __post_init__(self):
        if not self.portfolio_id:
            raise ValueError("portfolio_id is required")
        if not self.ticker or len(self.ticker) > 5:
            raise ValueError("ticker must be 1-5 chars")
        if self.type not in ("BUY", "SELL"):
            raise ValueError("type must be BUY or SELL")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.price < 0:
            raise ValueError("price must be semi-positive")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("currency must be 3-letters")
