from ..get_portfolio_by_id_query import GetPortfolioByIdQuery
from ..dto.dtos import PortfolioDto, PositionDto, TransactionDto

class GetPortfolioByIdHandler:
    
    def __init__(self, repository):
        self.repository = repository
        
    def handle(self, query: GetPortfolioByIdQuery) -> PortfolioDto:
        portfolio = self.repository.find_by_id(query.portfolio_id)
        if not portfolio:
            return None
            
        # Convert domain model to simple flat DTOs purely for read access
        positions_dto = []
        for pos in portfolio.positions():
            positions_dto.append(PositionDto(
                ticker=pos.ticker.symbol,
                quantity=pos.quantity.value,
                average_price=pos.average_price.amount,
                currency=pos.average_price.currency
            ))
            
        transactions_dto = []
        for t in portfolio._transactions:
            transactions_dto.append(TransactionDto(
                id=t.id,
                ticker=t.ticker.symbol,
                type_name=t.type.value,
                quantity=t.quantity.value,
                price=t.price.amount,
                currency=t.price.currency,
                date_iso=t._date.isoformat()
            ))
            
        return PortfolioDto(
            id=portfolio.id,
            owner_id=portfolio._owner_id,
            status=portfolio.status,
            positions=positions_dto,
            transactions=transactions_dto
        )
