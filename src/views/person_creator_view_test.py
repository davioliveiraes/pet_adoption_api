from typing import Dict
import pytest
from .person_creator_view import PersonCreatorView
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class MockPersonCreatorController:
    def create(self, person_info: Dict) -> Dict:
        return {
            "data": {
                "type": "Person",
                "count": 1,
                "attributes": person_info
            }
        }

class MockPersonCreatorControllerError:
    def create(self, person_info: Dict) -> Dict:
        raise Exception("Erro ao criar pessoa")

def test_handle():
    person_info = {
        "first_name": "Harvey",
        "last_name": "Specter",
        "age": 30,
        "pet_id": 123
    }

    http_request = HttpRequest(body=person_info)
    controller = MockPersonCreatorController()
    view = PersonCreatorView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 201
    assert response.body["data"]["type"] == "Person"
    assert response.body["data"]["count"] == 1
    assert response.body["data"]["attributes"] == person_info

def test_handle_with_invalid_data():
    person_info = {
        "first_name": "Harvey123",
        "last_name": "Specter",
        "age": 30,
        "pet_id": 123
    }

    http_request = HttpRequest(body=person_info)
    controller = MockPersonCreatorControllerError()
    view = PersonCreatorView(controller) # type: ignore

    with pytest.raises(Exception):
        view.handle(http_request)

def test_handle_response_structure():
    person_info = {
        "first_name": "Mike",
        "last_name": "Ross",
        "age": 25,
        "pet_id": 456
    }

    http_request = HttpRequest(body=person_info)
    controller = MockPersonCreatorController()
    view = PersonCreatorView(controller) # type: ignore

    response = view.handle(http_request)

    assert hasattr(response, 'status_code')
    assert hasattr(response, 'body')
    assert "data" in response.body
    assert "type" in response.body["data"]
    assert "count" in response.body["data"]
    assert "attributes" in response.body["data"]
