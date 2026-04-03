from ..add_transaction_command import AddTransactionCommand

class AddTransactionHandler:
    
    def __init__(self, repository):
        self.repository = repository
        
    def handle(self, command: AddTransactionCommand) -> str:
        # Load from repo
        portfolio = self.repository.find_by_id(command.portfolio_id)
        if not portfolio:
            raise ValueError(f"Portfolio {command.portfolio_id} not found")
            
        # Execute business logic on the aggregate
        tx_id = portfolio.add_transaction(
            ticker_str=command.ticker,
            type_name=command.type,
            quantity_val=command.quantity,
            price_val=command.price,
            currency=command.currency
        )
        
        # Save changes
        self.repository.save(portfolio)
        
        return tx_id
