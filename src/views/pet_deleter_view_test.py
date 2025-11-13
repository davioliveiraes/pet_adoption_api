import pytest
from .pet_deleter_view import PetDeleterView
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse

class MockDeleteController:
    def delete(self, name: str) -> None:
        pass

class MockPetDeleteControllerError:
    def delete(self, name: str) -> None:
        raise Exception("Pet nao encontrado")

def test_handle():
    pet_name = "Kurama"

    http_request = HttpRequest(param={"name": pet_name})
    controller = MockDeleteController()
    view = PetDeleterView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 204

def test_handle_with_nonexistent_pet():
    pet_name = "Pet Inexistente"

    http_request = HttpRequest(param={"name": pet_name})
    controller = MockPetDeleteControllerError()
    view = PetDeleterView(controller) # type: ignore

    with pytest.raises(Exception):
        view.handle(http_request)

def test_handle_response_structure():
    pet_name = "Susano"

    http_request = HttpRequest(param={"name": pet_name})
    controller = MockDeleteController()
    view = PetDeleterView(controller) # type: ignore

    response = view.handle(http_request)

    assert hasattr(response, "status_code")
    assert response.status_code == 204

def test_handle_with_empty_name():
    pet_name = ""

    http_request = HttpRequest(param={"name": pet_name})
    controller = MockDeleteController()
    view = PetDeleterView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 204

def test_handle_with_special_characters_in_name():
    pet_name = "Kurama-2025"

    http_request = HttpRequest(param={"name": pet_name})
    controller = MockDeleteController()
    view = PetDeleterView(controller) # type: ignore

    response = view.handle(http_request)

    assert isinstance(response, HttpResponse)
    assert response.status_code == 204
