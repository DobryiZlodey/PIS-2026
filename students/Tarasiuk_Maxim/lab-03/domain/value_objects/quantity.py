from dataclasses import dataclass

@dataclass(frozen=True)
class Quantity:
    """Value Object: Количество ценных бумаг"""
    
    value: int
    
    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Quantity must be an integer")
        if self.value <= 0:
            raise ValueError(f"Quantity must be greater than zero: {self.value}")
            
    def add(self, amount: int):
        return Quantity(self.value + amount)
        
    def subtract(self, amount: int):
        if self.value - amount < 0:
            raise ValueError("Quantity cannot be negative after subtraction")
        return Quantity(self.value - amount)
