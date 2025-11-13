from typing import Dict
import pytest
from .person_finder_view import PersonFinderView
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class MockPersonFinderController:
    def find(self, person_id: int) -> Dict:
        return {
            "data": {
                "type": "Person",
                "count": 1,
                "attributes": {
                    "person_id": person_id,
                    "fist_name": "Harvey",
                    "last_name": "Specter",
                    "age": 30,
                    "pet_id": 123
                }
            }
        }

class MockPersonFinderControllerError:
    def find(self, person_id: int) -> Dict:
        raise Exception("Pessoa nao encontrada")

def test_handle():
    person_id = 1

    http_request = HttpRequest(param={"person_id": person_id})
    controller = MockPersonFinderController()
    view = PersonFinderView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"]["type"] == "Person"
    assert response.body["data"]["count"] == 1
    assert response.body["data"]["attributes"]["person_id"] == person_id

def test_handle_with_invalid_person_id():
    person_id = 999

    http_request = HttpRequest(param={"person_id": person_id})
    controller = MockPersonFinderControllerError()
    view = PersonFinderView(controller) # type: ignore

    with pytest.raises(Exception):
        view.handle(http_request)

def test_handle_response_structure():
    person_id = 2

    http_request = HttpRequest(param={"person_id": person_id})
    controller = MockPersonFinderController()
    view = PersonFinderView(controller) # type: ignore

    response = view.handle(http_request)

    assert hasattr(response,"status_code")
    assert hasattr(response, "body")
    assert "data" in response.body
    assert "type" in response.body["data"]
    assert "count" in response.body["data"]
    assert "attributes" in response.body["data"]
