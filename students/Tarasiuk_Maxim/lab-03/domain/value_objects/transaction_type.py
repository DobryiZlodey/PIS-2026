from enum import Enum

class TransactionType(Enum):
    """Value Object: Тип транзакции (Перечисление)"""
    BUY = "BUY"
    SELL = "SELL"
