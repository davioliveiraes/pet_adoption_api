from abc import ABC, abstractmethod

class PetDeleteControllerInterface(ABC):

    @abstractmethod
    def delete(self, name: str) -> None:
        pass
