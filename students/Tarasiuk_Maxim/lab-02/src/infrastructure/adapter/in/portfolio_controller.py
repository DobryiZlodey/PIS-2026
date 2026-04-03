class PortfolioController:
    """Точка входа (Inbound Adapter): Например, REST Controller"""
    
    def __init__(self, use_case):
        self.use_case = use_case
        
    def get_profitability(self, portfolio_id: str, start_date_str: str, end_date_str: str):
        """Эндпоинт для получения доходности"""
        # В реальной системе здесь парсинг дат и обработка HTTP запроса
        # command = CalculateProfitabilityCommand(...)
        # return self.use_case.calculate(command)
        pass
