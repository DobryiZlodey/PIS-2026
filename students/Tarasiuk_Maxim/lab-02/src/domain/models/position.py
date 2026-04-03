class Position:
    """Доменная модель: Позиция по ценной бумаге"""
    
    def __init__(self, ticker: str, amount: int, average_price: float):
        self.ticker = ticker
        self.amount = amount
        self.average_price = average_price
