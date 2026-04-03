import json
from src.students.Tarasiuk_Maxim.lab_07.cqrs.read_model.portfolio_view import PortfolioViewOrm

class PortfolioProjectionHandler:
    """Event-Driven Synchronization handlers"""
    
    def __init__(self, db_session):
        self.db = db_session
        
    def handle_portfolio_created(self, event) -> None:
        """
        Event payload assumed: {portfolio_id, owner_id, timestamp}
        """
        db_view = PortfolioViewOrm(
            portfolio_id=event.portfolio_id,
            owner_id=event.owner_id,
            status="ACTIVE",
            total_positions_count=0,
            view_data=json.dumps({"positions": [], "transactions": []})
        )
        self.db.add(db_view)
        self.db.commit()

    def handle_transaction_added(self, event) -> None:
        """
        Event payload assumed: {portfolio_id, tx_id, ticker, type, quantity, price, currency, timestamp}
        """
        # Load projection
        db_view = self.db.query(PortfolioViewOrm).filter(PortfolioViewOrm.portfolio_id == event.portfolio_id).first()
        if not db_view:
            return # Should not happen unless events out of order, in real system: retry or DLQ
            
        data = json.loads(db_view.view_data)
        
        # update transactions list
        data["transactions"].append({
            "id": event.tx_id,
            "ticker": event.ticker,
            "type": event.type,
            "quantity": event.quantity,
            "price": event.price,
            "currency": event.currency,
            "date": event.timestamp.isoformat()
        })
        
        # simplified rolling update of positions view
        ticker = event.ticker
        qty = event.quantity if event.type == "BUY" else -event.quantity
        
        pos_found = False
        for p in data["positions"]:
            if p["ticker"] == ticker:
                p["quantity"] += qty
                pos_found = True
                break
        
        if not pos_found and qty > 0:
            data["positions"].append({"ticker": ticker, "quantity": qty, "average_price": event.price})
            db_view.total_positions_count += 1
            
        db_view.view_data = json.dumps(data)
        self.db.commit()
    
    def handle_portfolio_closed(self, event) -> None:
        db_view = self.db.query(PortfolioViewOrm).filter(PortfolioViewOrm.portfolio_id == event.portfolio_id).first()
        if db_view:
            db_view.status = "CLOSED"
            self.db.commit()
