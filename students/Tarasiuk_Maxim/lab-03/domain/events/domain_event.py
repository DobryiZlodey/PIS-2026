from abc import ABC, abstractmethod
from datetime import datetime

class DomainEvent(ABC):
    """Базовый класс для всех доменных событий"""
    
    @abstractmethod
    def occurred_on(self) -> datetime:
        pass
