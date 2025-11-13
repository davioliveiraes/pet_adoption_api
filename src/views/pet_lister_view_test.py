from typing import Dict
import pytest
from .pet_lister_view import PetListerView
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class MockPetListerController():
    def list(self) -> Dict:
        return {
            "data": {
                "type": "Pets",
                "count": 3,
                "attributes": [
                    {
                        "pet_id": 1,
                        "name": "Kurama",
                        "type": "cat",
                        "age": 3
                    },
                    {
                        "pet_id": 2,
                        "name": "Gobi",
                        "type": "Dog",
                        "age": 2
                    },
                    {
                        "pet_id": 3,
                        "name": "Nibi",
                        "type": "cat",
                        "age": 4
                    }
                ]
            }
        }

class MockPetListerControllerEmpty():
    def list(self) -> Dict:
        return {
            "data": {
                "type": "Pets",
                "count": 0,
                "attributes": []
            }
        }

class MockPetListerControllerError():
    def list(self) -> Dict:
        raise Exception("Erro ao listar pets")

def test_handle():
    http_request = HttpRequest()
    controller = MockPetListerController()
    view = PetListerView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"]["type"] == "Pets"
    assert response.body["data"]["count"] == 3
    assert len(response.body["data"]["attributes"]) == 3

def test_handle_with_empty_list():
    http_request = HttpRequest()
    controller = MockPetListerControllerEmpty()
    view = PetListerView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.body["data"]["count"] == 0
    assert response.body["data"]["attributes"] == []

def test_handle_with_error():
    http_request = HttpRequest()
    controller = MockPetListerControllerError()
    view = PetListerView(controller) # type: ignore

    with pytest.raises(Exception):
        view.handle(http_request)

def test_handle_response_structure():
    http_request = HttpRequest()
    controller = MockPetListerController()
    view = PetListerView(controller) # type: ignore

    response = view.handle(http_request)

    assert hasattr(response, "status_code")
    assert hasattr(response, "body")
    assert "data" in response.body
    assert "type" in response.body["data"]
    assert "count" in response.body["data"]
    assert "attributes" in response.body["data"]


def test_handle_pets_attributes():
    http_request = HttpRequest()
    controller = MockPetListerController()
    view = PetListerView(controller) # type: ignore

    response = view.handle(http_request)

    first_pet = response.body["data"]["attributes"][0]

    assert "pet_id" in first_pet
    assert "name" in first_pet
    assert "type" in first_pet
    assert "age" in first_pet
    assert first_pet["name"] == "Kurama"
    assert first_pet["type"] == "cat"

def test_handle_multiple_pets():
    http_request = HttpRequest()
    controller = MockPetListerController()
    view = PetListerView(controller) # type: ignore

    response = view.handle(http_request)

    pets = response.body["data"]["attributes"]

    assert len(pets) > 0
    assert all("pet_id" in pet for pet in pets)
    assert all("name" in pet for pet in pets)
