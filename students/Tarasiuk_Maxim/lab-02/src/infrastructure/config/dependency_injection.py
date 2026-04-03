from src.infrastructure.adapter.out.in_memory_portfolio_repository import InMemoryPortfolioRepository
from src.infrastructure.adapter.out.fake_market_data_service import FakeMarketDataService
from src.application.service.portfolio_service import PortfolioService
from src.infrastructure.adapter.in.portfolio_controller import PortfolioController

class DependencyContainer:
    """Конфигурация DI: связывание портов и адаптеров"""
    
    def __init__(self):
        # Создаём исходящие адаптеры
        self.portfolio_repository = InMemoryPortfolioRepository()
        self.market_data_service = FakeMarketDataService()
        
        # Создаём application service с инжекцией зависимостей
        self.portfolio_service = PortfolioService(
            repository=self.portfolio_repository,
            market_data_service=self.market_data_service
        )
        
        # Создаем контроллер, передаем ему use-case
        self.portfolio_controller = PortfolioController(
            use_case=self.portfolio_service
        )
        
    def get_portfolio_controller(self):
        return self.portfolio_controller
