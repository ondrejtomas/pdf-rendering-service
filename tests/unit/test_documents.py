# Third Party
from asynctest import patch
from fastapi import HTTPException, UploadFile
from pytest import mark, raises

# Local
from src.routers.documents import upload_document


@mark.asyncio
async def test_upload_document_invalid_content_type():
    """ Tests whether method 'upload_document' returns proper response when sending non PDF file """

    upload_file = UploadFile(filename='test')

    with raises(HTTPException) as exp:
        await upload_document(upload_file)
        assert exp.status_code == 415


@mark.asyncio
@patch("src.routers.documents.DatabaseHandler")
@patch("src.routers.documents.normalize_document")
async def test_upload_document(mock_database_handler, mock_normalize_document):
    """ Tests whether method 'upload_document' returns proper response when sending proper PDF file """

    upload_file = UploadFile(filename='test',
                             content_type='application/pdf',
                             file=open('tests/resources/pages_num_3.pdf', "rb"))

    response = await upload_document(upload_file)

    assert len(response) == 1
    assert type(response["id"]) == str


# TODO: add other tests
