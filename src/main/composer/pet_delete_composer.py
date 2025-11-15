from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pets_repository import PetsRepository
from src.controllers.pets_delete_controller import PetDeleteController
from src.views.pet_deleter_view import PetDeleterView

def pet_delete_composer():
    model = PetsRepository(db_connection_handler)
    controller = PetDeleteController(model)
    view = PetDeleterView(controller)

    return view
