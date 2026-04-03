from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from src.students.Tarasiuk_Maxim.lab_05.infrastructure.config.database import Base

class PortfolioViewOrm(Base):
    __tablename__ = "portfolio_read_model"
    # Denormalized completely for ultrafast reads without JOINs
    
    portfolio_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    status = Column(String)
    
    # Materialized derived values
    total_positions_count = Column(Integer, default=0)
    
    # JSON payload holding positions and transactions details
    # SQLite fallback does not natively have JSONB, but if we assume Postgres is the target:
    view_data = Column(String) # For SQLite testability. In Postgres: Column(JSONB)
