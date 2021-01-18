# Standard Library
from base64 import b64decode
from io import BytesIO
from logging import getLogger
from typing import List

# Third Party
from dramatiq import actor
from fitz import open as open_pdf
from PIL import Image
from resizeimage.resizeimage import resize_contain

# Local
from src.common import settings
from src.common.enums import DocumentStatus
from src.database.handler import DatabaseHandler
from src.message_queue.handler import MessageQueueHandler

logger = getLogger(__name__)


# TODO: enable actor configuration via env. variables
@actor(broker=MessageQueueHandler().broker, max_retries=3, time_limit=60000)
def normalize_document(document_id: str, document_name: str, document_content_encoded: str):
    logger.info(f"({document_id}) Processing document named '{document_name}'.")

    # change the status of the document from IN_QUEUE to PROCESSING
    DatabaseHandler().update_document(document_id=document_id, document_status=DocumentStatus.PROCESSING)

    # convert PDF document to PNG images (pages)
    pages_data = get_document_pages(document_content_encoded=document_content_encoded)

    # save pages of the document to the database
    DatabaseHandler().insert_pages(document_id=document_id, pages_data=pages_data)

    # change the status of the document from PROCESSING to DONE and save the rendered pages
    DatabaseHandler().update_document(document_id=document_id, document_status=DocumentStatus.DONE)

    logger.info(f"({document_id}) Document named '{document_name}' was processed.")


def get_document_pages(document_content_encoded: str) -> List[bytes]:
    # decode the content of the document
    document_content = b64decode(document_content_encoded)

    # extract the PDF file
    pdf = open_pdf(stream=document_content, filetype="pdf")

    # convert PDF document to PNG images (bytes)
    images_original = (page.getPixmap().getPNGdata() for page in pdf)

    # reduce size of each image to fit the max width and max height
    images_reduced = []
    for image_original in images_original:
        # prepare streams of data
        image_original_stream = BytesIO(image_original)
        image_reduced_stream = BytesIO()

        # convert original image stream to PIL image format
        image_original_pil = Image.open(image_original_stream)

        # resize the image to fit
        image_reduced_pil = resize_contain(image_original_pil,
                                           [settings.RENDERING_PNG_MAX_WIDTH, settings.RENDERING_PNG_MAX_HEIGHT])

        # convert the resized PIL image back to stream and then back to bytes
        image_reduced_pil.save(image_reduced_stream, format='PNG')
        image_reduced = image_reduced_stream.getvalue()

        # add to the list of converted pages
        images_reduced.append(image_reduced)

    return images_reduced
