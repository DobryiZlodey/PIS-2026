from datetime import datetime

class Transaction:
    """Доменная модель: Сделка"""
    
    def __init__(self, transaction_id: str, ticker: str, type: str, volume: int, price: float, date: datetime):
        self.id = transaction_id
        self.ticker = ticker
        self.type = type # 'BUY' or 'SELL'
        self.volume = volume
        self.price = price
        self.date = date
