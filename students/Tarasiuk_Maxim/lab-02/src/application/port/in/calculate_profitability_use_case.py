from abc import ABC, abstractmethod
from datetime import datetime

class CalculateProfitabilityCommand:
    """DTO для расчета доходности портфеля"""
    def __init__(self, portfolio_id: str, start_date: datetime, end_date: datetime):
        self.portfolio_id = portfolio_id
        self.start_date = start_date
        self.end_date = end_date

class CalculateProfitabilityUseCase(ABC):
    """Входящий порт: расчет доходности портфеля за период"""
    
    @abstractmethod
    def calculate(self, command: CalculateProfitabilityCommand) -> dict:
        """
        Рассчитывает доходность портфеля
        :param command: Данные для расчета
        :return: Детализированный отчет с доходностью (dict для примера)
        """
        pass
