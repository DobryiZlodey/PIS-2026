from typing import List
import logging

from src.students.Tarasiuk_Maxim.lab_03.domain.events.domain_event import DomainEvent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InMemoryEventPublisher:
    """Простой публикатор событий, логирующий произошедшие доменные события"""
    
    def publish(self, events: List[DomainEvent]) -> None:
        if not events:
            return
            
        for event in events:
            logger.info(f"Published Event: {event.__class__.__name__} -> {event.__dict__}")
