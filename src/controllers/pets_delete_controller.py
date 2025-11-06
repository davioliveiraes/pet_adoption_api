from src.models.sqlite.interfeces.pets_repository import PetsRepositoryInterface

class PetDeleteController:
    def __init__(self, pet_repository: PetsRepositoryInterface) -> None:
        self.__pet_repository = pet_repository

    def delete(self, name: str) -> None:
        self.__pet_repository.delete_pets(name)
