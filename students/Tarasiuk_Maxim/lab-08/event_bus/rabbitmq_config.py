import json
import logging

class RabbitMQMockPublisher:
    """
    Mock integration for RabbitMQ Event Bus. 
    In real production this would wrap aio-pika or pika.
    """
    def __init__(self, exchange_name='portfolio_events'):
        self.exchange = exchange_name
        self.logger = logging.getLogger(__name__)

    def publish(self, routing_key: str, message: dict):
        """
        Publishes a message to the unified Exchange with a specific topic/key.
        """
        payload = json.dumps(message)
        self.logger.info(f"[RabbitMQ] Published to '{self.exchange}' with key '{routing_key}': {payload}")
        # Imagine pika.BlockingConnection here
        # channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=payload)

class RabbitMQMockConsumer:
    """
    Consumer logic for listening to topics.
    """
    def __init__(self, queue_name, routing_keys):
        self.queue = queue_name
        self.keys = routing_keys
        self.logger = logging.getLogger(__name__)
        
    def start_consuming(self, callback):
        self.logger.info(f"[RabbitMQ] Started listening on queue '{self.queue}' for keys: {self.keys}")
        # Imagine channel.basic_consume(queue=self.queue, on_message_callback=callback)
        # channel.start_consuming()
