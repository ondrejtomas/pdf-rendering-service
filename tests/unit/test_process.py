# Local
from src.core.process import get_document_pages


def test_get_document_pages():
    """ Tests whether method 'get_document_pages' split PDF in encoded bytes and returns pages """

    document_content_encoded = open('tests/resources/pages_num_3_encoded.txt').read()

    pages_data = get_document_pages(document_content_encoded=document_content_encoded)

    assert len(pages_data) == 3

    # TODO: test content of the images


# TODO: add other tests
