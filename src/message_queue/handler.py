# Standard Library
from logging import getLogger

# Third Party
from dramatiq import set_broker
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from pika.credentials import PlainCredentials

# Local
from src.common import settings
from src.common.utils import Singleton

logger = getLogger(__name__)


class MessageQueueHandler(metaclass=Singleton):
    # (TODO: make this class abstract and implement specific handlers)

    def __init__(self):
        # create RabbitMQ broker
        self.broker = RabbitmqBroker(host=settings.MESSAGE_QUEUE_HOST,
                                     port=settings.MESSAGE_QUEUE_PORT,
                                     credentials=PlainCredentials(username=settings.MESSAGE_QUEUE_USERNAME,
                                                                  password=settings.MESSAGE_QUEUE_PASSWORD))

        # set the broker as default
        set_broker(self.broker)

    def close(self):
        # close connection to the broker
        self.broker.close()
