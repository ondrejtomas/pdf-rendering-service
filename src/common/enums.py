# Standard Library
from enum import Enum


class DocumentStatus(Enum):
    IN_QUEUE = "IN_QUEUE"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
