# Standard Library
from logging import getLogger
from typing import Dict

# Third Party
from fastapi.routing import APIRouter

# Local
from src.common import constants

logger = getLogger(__name__)

router = APIRouter()


@router.get("/", tags=["service-info"])
def root() -> Dict[str, str]:
    return {"message": constants.SERVICE_DESCRIPTION}


@router.get("/healthcheck", tags=["service-info"])
def healthcheck() -> Dict[str, str]:
    # TODO: check that everything is alright
    return {"status": "ok"}


@router.get("/ready", tags=["service-info"])
def ready() -> Dict[str, str]:
    # TODO: check that service is ready to process incoming requests (e.g. if database is ready)
    return {"status": "ok"}
