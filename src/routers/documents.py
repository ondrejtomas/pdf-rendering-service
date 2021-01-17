# Standard Library
from base64 import b64encode
from io import BytesIO
from logging import getLogger
from uuid import uuid4

# Third Party
from fastapi import File, HTTPException, UploadFile
from fastapi.routing import APIRouter
from starlette.responses import StreamingResponse

# Local
from src.common.enums import DocumentStatus
from src.core.process import normalize_document
from src.database.handler import DatabaseHandler

logger = getLogger(__name__)

router = APIRouter()


@router.post("/", tags=["documents"])
async def upload_document(document: UploadFile = File(...)):
    document_id = str(uuid4())

    logger.info(
        f"({document_id}) Document named '{document.filename}' succesfully uploaded and is ready to be processed.")

    # check whether the document has valid format (PDF)
    if document.content_type != 'application/pdf':
        logger.debug(f"({document_id}) Invalid document content type '{document.filename}'.")
        raise HTTPException(
            status_code=415,
            detail=f"Invalid document content type '{document.content_type}', only 'application/pdf' is supported.")

    # save header of the document to the database
    DatabaseHandler().insert_document(document_id=document_id, document_name=document.filename)

    # read and encode the content of the document
    document_content = await document.read()
    document_content_encoded = b64encode(document_content).decode('ascii')

    # offload the document processing
    normalize_document.send(document_id=document_id,
                            document_name=document.filename,
                            document_content_encoded=document_content_encoded)

    return {"id": document_id}


@router.get("/{document_id}", tags=["documents"])
async def get_document(document_id: str):
    # get the document from database
    document = DatabaseHandler().get_document(document_id=document_id)

    # check whether the document of given id exists
    if not document:
        logger.debug(f"({document_id}) Document does not exist.")
        raise HTTPException(status_code=404, detail=f"Document does not exist.")

    return {"name": document.name, "pages_number": document.pages_number, "status": document.status}


@router.get("/{document_id}/pages/{page_id}", tags=["documents"])
async def get_page(document_id: str, page_id: str):
    # get the document first and check its status
    document = await get_document(document_id)
    if document["status"] != DocumentStatus.DONE.value:
        logger.debug(f"({document_id}) Document has not been processed yet.")
        raise HTTPException(status_code=404, detail=f"Document has not been processed yet.")

    # get the page from database
    page = DatabaseHandler().get_page(document_id=document_id, page_id=page_id)

    # check whether the page of given id exists
    if not page:
        logger.debug(f"({document_id}, {page_id}) Page does not exist.")
        raise HTTPException(status_code=404, detail=f"Page does not exist.")

    return StreamingResponse(BytesIO(page.data), media_type="image/png")
