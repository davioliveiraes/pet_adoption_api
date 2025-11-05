# pylint: disable=W0613:unused-argument
from .person_finder_controller import PersonFinderController

class MockPerson():
    def __init__(self, first_name, last_name, pet_name, pet_type) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.pet_name = pet_name
        self.pet_type = pet_type

class MockPeopleRepository:
    def get_person(self, person_id: int):
        return MockPerson(
            first_name="Naruto",
            last_name="Uzumaki",
            pet_name="Kurama",
            pet_type="fox"
        )

def test_find():
    controller = PersonFinderController(MockPeopleRepository()) # type: ignore
    response = controller.find(123)

    expected_response = {
        "data": {
            "type": "Person",
            "count": 1,
            "attributes": {
                "first_name": "Naruto",
                "last_name": "Uzumaki",
                "pet_name": "Kurama",
                "pet_type": "fox"
            }
        }
    }

    assert response == expected_response
