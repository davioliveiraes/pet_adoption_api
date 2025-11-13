from unittest import mock
import pytest
from sqlalchemy.orm.exc import NoResultFound # type: ignore
from src.models.sqlite.entities.people import PeopleTable
from .people_repository import PeopleRepository

class MockConnection:
    def __init__(self) -> None:
        self.session = mock.MagicMock()

        mock_person = mock.MagicMock(
            first_name="test name",
            last_name="last name",
            pet_name="cao",
            pet_type="dog"
        )

        (self.session.query.return_value
         .outerjoin.return_value
         .filter.return_value
         .with_entities.return_value
         .one.return_value) = mock_person

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class MockConnectionNoResult:
    def __init__(self) -> None:
        self.session = mock.MagicMock()

        (self.session.query.return_value
         .outerjoin.return_value
         .filter.return_value
         .with_entities.return_value
         .one.side_effect) = NoResultFound("No result found")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class MockConnectionForInsert:
    def __init__(self) -> None:
        self.session = mock.MagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def test_insert_person():
    """Testa a inserção de uma pessoa no banco de dados"""
    mock_connection = MockConnectionForInsert()
    repo = PeopleRepository(mock_connection)

    repo.insert_person(
        first_name="test name",
        last_name="last name",
        age=30,
        pet_id=2
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()
    mock_connection.session.rollback.assert_not_called()

    call_args = mock_connection.session.add.call_args[0][0]
    assert call_args.first_name == "test name"
    assert call_args.last_name == "last name"
    assert call_args.age == 30
    assert call_args.pet_id == 2

def test_insert_person_error():
    """Testa o tratamento de erro ao inserir uma pessoa"""
    mock_connection = MockConnectionForInsert()
    mock_connection.session.commit.side_effect = Exception("Database error")

    repo = PeopleRepository(mock_connection)

    with pytest.raises(Exception):
        repo.insert_person(
            first_name="test name",
            last_name="last name",
            age=30,
            pet_id=2
        )

    mock_connection.session.rollback.assert_called_once()

def test_get_person():
    """Testa a busca de uma pessoa por ID"""
    mock_connection = MockConnection()
    repo = PeopleRepository(mock_connection)

    response = repo.get_person(person_id=2)

    mock_connection.session.query.assert_called_once_with(PeopleTable)

    assert response.first_name == "test name" # type: ignore
    assert response.last_name == "last name" # type: ignore
    assert response.pet_name == "cao"
    assert response.pet_type == "dog"

def test_get_person_no_result():
    """Testa busca de pessoa quando não há resultado"""
    mock_connection = MockConnectionNoResult()
    repo = PeopleRepository(mock_connection)

    response = repo.get_person(person_id=99)

    mock_connection.session.query.assert_called_once_with(PeopleTable)

    assert response is None
