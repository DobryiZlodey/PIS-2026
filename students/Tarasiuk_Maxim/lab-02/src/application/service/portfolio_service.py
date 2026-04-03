from src.application.port.in.calculate_profitability_use_case import CalculateProfitabilityUseCase, CalculateProfitabilityCommand

class PortfolioService(CalculateProfitabilityUseCase):
    """Реализация use-cases для управления портфелем"""
    
    def __init__(self, repository, market_data_service):
        self.repository = repository
        self.market_data_service = market_data_service
        
    def calculate(self, command: CalculateProfitabilityCommand) -> dict:
        # TODO: реализовать в Lab #4
        # 1. Загрузить портфель через repository
        # 2. Получить актуальные цены через market_data_service
        # 3. Произвести вычисления (доменная логика)
        # 4. Сформировать и вернуть отчет
        raise NotImplementedError("Будет реализовано в Lab #4")
