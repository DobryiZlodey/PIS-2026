from ..command.create_portfolio_command import CreatePortfolioCommand
from ..command.add_transaction_command import AddTransactionCommand
from ..command.close_portfolio_command import ClosePortfolioCommand
from ..query.get_portfolio_by_id_query import GetPortfolioByIdQuery
from ..query.list_active_portfolios_query import ListActivePortfoliosQuery

from ..command.handlers.create_portfolio_handler import CreatePortfolioHandler
from ..command.handlers.add_transaction_handler import AddTransactionHandler
from ..command.handlers.close_portfolio_handler import ClosePortfolioHandler
from ..query.handlers.get_portfolio_by_id_handler import GetPortfolioByIdHandler
from ..query.handlers.list_active_portfolios_handler import ListActivePortfoliosHandler
from ..query.dto.dtos import PortfolioDto

class PortfolioService:
    """Facade: Прикладной сервис работы с портфелями инвестиций"""
    
    def __init__(self, repository):
        # Initialize handlers
        self._create_handler = CreatePortfolioHandler(repository)
        self._add_transaction_handler = AddTransactionHandler(repository)
        self._close_handler = ClosePortfolioHandler(repository)
        
        self._get_by_id_handler = GetPortfolioByIdHandler(repository)
        self._list_active_handler = ListActivePortfoliosHandler(repository)

    # Commands
    def create_portfolio(self, command: CreatePortfolioCommand) -> str:
        return self._create_handler.handle(command)
        
    def add_transaction(self, command: AddTransactionCommand) -> str:
        return self._add_transaction_handler.handle(command)
        
    def close_portfolio(self, command: ClosePortfolioCommand) -> None:
        self._close_handler.handle(command)
        
    # Queries
    def get_portfolio_by_id(self, query: GetPortfolioByIdQuery) -> PortfolioDto:
        return self._get_by_id_handler.handle(query)
        
    def list_active_portfolios(self, query: ListActivePortfoliosQuery) -> list[PortfolioDto]:
        return self._list_active_handler.handle(query)
