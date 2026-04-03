from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    """Value Object: Денежная сумма"""
    
    amount: float
    currency: str
    
    def __post_init__(self):
        if not isinstance(self.amount, (int, float)):
            raise ValueError(f"Amount must be a number: {self.amount}")
        if self.amount < 0:
            raise ValueError(f"Amount cannot be negative: {self.amount}")
        if not isinstance(self.currency, str) or len(self.currency) != 3:
            raise ValueError(f"Currency must be a 3-letter string: {self.currency}")
            
    def __add__(self, other):
        if not isinstance(other, Money):
            raise ValueError("Can only add Money to Money")
        if self.currency != other.currency:
            raise ValueError("Cannot add Money of different currencies")
        return Money(self.amount + other.amount, self.currency)
        
    def __sub__(self, other):
        if not isinstance(other, Money):
            raise ValueError("Can only subtract Money from Money")
        if self.currency != other.currency:
            raise ValueError("Cannot subtract Money of different currencies")
        if self.amount < other.amount:
            raise ValueError("Resulting amount cannot be negative")
        return Money(self.amount - other.amount, self.currency)
