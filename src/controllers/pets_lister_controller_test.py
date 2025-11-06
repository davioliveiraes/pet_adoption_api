from src.models.sqlite.entities.pets import PetsTable
from src.controllers.pets_lister_controller import PetListerController

class MockPetsRepository:
    def list_pets(self):
        return [
            PetsTable(name="Theo", type="cat", id=4),
            PetsTable(name="Back", type="dog", id=47),
        ]

def test_list_pets():
    controller = PetListerController(MockPetsRepository()) # type: ignore
    response = controller.list()

    expected_response = {
        "data": {
            "type": "Pets",
            "count": 2,
            "attributes": [
                { "name": "Theo", "id": 4 },
                { "name": "Back", "id": 47 }
            ]
        }
    }

    assert response == expected_response
