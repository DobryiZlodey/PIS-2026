from typing import List
from ..list_active_portfolios_query import ListActivePortfoliosQuery
from ..dto.dtos import PortfolioDto, PositionDto, TransactionDto
from .get_portfolio_by_id_handler import GetPortfolioByIdHandler

class ListActivePortfoliosHandler:
    
    def __init__(self, repository):
        self.repository = repository
        # Re-use logic or manual mapping
        self.single_handler = GetPortfolioByIdHandler(repository)
        
    def handle(self, query: ListActivePortfoliosQuery) -> List[PortfolioDto]:
        portfolios = self.repository.find_all_active()
        
        # Apply pagination (in memory for mock, in DB for real)
        portfolios_page = portfolios[query.offset : query.offset + query.limit]
        
        dtos = []
        for p in portfolios_page:
            # We map the domain portfolio to DTO directly
            positions_dto = []
            for pos in p.positions():
                positions_dto.append(PositionDto(
                    ticker=pos.ticker.symbol,
                    quantity=pos.quantity.value,
                    average_price=pos.average_price.amount,
                    currency=pos.average_price.currency
                ))
            
            transactions_dto = []
            for t in p._transactions:
                transactions_dto.append(TransactionDto(
                    id=t.id,
                    ticker=t.ticker.symbol,
                    type_name=t.type.value,
                    quantity=t.quantity.value,
                    price=t.price.amount,
                    currency=t.price.currency,
                    date_iso=t._date.isoformat()
                ))
                
            dtos.append(PortfolioDto(
                id=p.id,
                owner_id=p._owner_id,
                status=p.status,
                positions=positions_dto,
                transactions=transactions_dto
            ))
            
        return dtos
