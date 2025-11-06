from src.controllers.pets_delete_controller import PetDeleteController

def test_delete_pet(mocker):
    mock_repository = mocker.Mock()
    controller = PetDeleteController(mock_repository)
    controller.delete("Amigo")

    mock_repository.delete_pets.assert_called_once_with("Amigo")
