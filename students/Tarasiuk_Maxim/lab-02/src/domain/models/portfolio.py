class Portfolio:
    """Доменная модель: Портфель инвестора"""
    
    def __init__(self, portfolio_id: str, owner_id: str):
        self.id = portfolio_id
        self.owner_id = owner_id
        self.positions = []
        self.transactions = []
        
    def add_position(self, position):
        """Добавить позицию в портфель"""
        self.positions.append(position)
        
    def add_transaction(self, transaction):
        """Добавить сделку в историю портфеля"""
        self.transactions.append(transaction)
