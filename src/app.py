# Standard Library
from logging import getLogger

# Third Party
from fastapi import FastAPI
from uvicorn import Config, Server

# Local
from src.common import settings
from src.common.utils import setup_logging
from src.database.handler import DatabaseHandler
from src.message_queue.handler import MessageQueueHandler
from src.routers.documents import router as documents_router
from src.routers.root import router as root_router

setup_logging()
logger = getLogger(__name__)

# new FastAPI instance
app = FastAPI()

# link FastAPI routers
app.include_router(root_router)
app.include_router(documents_router, prefix="/documents")


@app.on_event("startup")
async def startup():
    # create database handler
    database_handler = DatabaseHandler()

    # create message queue handler
    message_queue_handler = MessageQueueHandler()


@app.on_event("shutdown")
async def shutdown():
    # close message queue handler
    database_handler.close()

    # close message queue handler
    message_queue_handler.close()


# custom uvicorn instance to extract the event loop
def start_uvicorn():
    uvicorn_config = Config('src.app:app',
                            host=settings.SERVICE_HOST,
                            port=settings.SERVICE_PORT,
                            log_level=settings.SERVICE_LOG_LEVEL.lower(),
                            loop="asyncio")
    server = Server(config=uvicorn_config)
    server.run()


if __name__ == "__main__":
    start_uvicorn()
