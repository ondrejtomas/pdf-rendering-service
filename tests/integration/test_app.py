# Standard Library
from time import sleep

# Third Party
from requests import get, post


def test_documents_endpoints():
    """ Tests calling '/documents' endpoint with PDF file and then '/documents/{document_id}'
        and finally '/documents/{document_id}/pages/{page_id}'"""

    files = {'document': ('pages_num_3.pdf', open('tests/resources/pages_num_3.pdf', 'rb'), 'application/pdf')}

    # upload the document via '/documents' endpoint
    response = post('http://localhost:8000/documents/', files=files)
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert "id" in response_json

    # save the document id
    document_id = response_json["id"]

    # sleep 5 secs to be sure that the document is processed
    sleep(5)

    # get status of the document via '/documents/{document_id}' endpoint
    response = get(f'http://localhost:8000/documents/{document_id}')
    response_json = response.json()

    assert response.status_code == 200
    assert response_json == {'name': 'pages_num_3.pdf', 'pages_number': 3, 'status': 'DONE'}

    # get the first page of the document via '/documents/{document_id}/pages/{page_id}' endpoint
    response = get(f'http://localhost:8000/documents/{document_id}/pages/1')

    assert response.status_code == 200
    assert "PNG" in str(response.content[0:10])


# TODO: add other tests
