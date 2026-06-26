import pytest

from app.services.user_service import UserService


@pytest.fixture()
def service(db_session):
    return UserService(session=db_session)


@pytest.fixture()
def existing_user(service):
    return service.create_user("johndoe", "secret", email="john@example.com", full_name="John Doe")


def test_create_user(service):
    user = service.create_user("johndoe", "secret")

    assert user.id is not None
    assert user.username == "johndoe"
    assert user.disabled is False


def test_create_user_hashes_password(service):
    user = service.create_user("johndoe", "secret")

    assert user.hashed_password != "secret"
    assert len(user.hashed_password) > 0


def test_create_user_with_optional_fields(service):
    user = service.create_user("johndoe", "secret", email="j@example.com", full_name="John")

    assert user.email == "j@example.com"
    assert user.full_name == "John"


def test_list_users_empty(service):
    assert service.list_users() == []


def test_list_users(service):
    service.create_user("alice", "pw1")
    service.create_user("bob", "pw2")

    assert len(service.list_users()) == 2


def test_get_user_found(service, existing_user):
    result = service.get_user(existing_user.id)

    assert result is not None
    assert result.username == "johndoe"


def test_get_user_not_found(service):
    assert service.get_user(999) is None


def test_get_by_username_found(service, existing_user):
    result = service.get_by_username("johndoe")

    assert result is not None
    assert result.id == existing_user.id


def test_get_by_username_not_found(service):
    assert service.get_by_username("nobody") is None


def test_update_user_username(service, existing_user):
    updated = service.update_user(existing_user.id, username="janedoe")

    assert updated.username == "janedoe"


def test_update_user_password(service, existing_user):
    old_hash = existing_user.hashed_password

    updated = service.update_user(existing_user.id, password="newpassword")

    assert updated.hashed_password != old_hash


def test_update_user_email(service, existing_user):
    updated = service.update_user(existing_user.id, email="new@example.com")

    assert updated.email == "new@example.com"


def test_update_user_full_name(service, existing_user):
    updated = service.update_user(existing_user.id, full_name="Jane Doe")

    assert updated.full_name == "Jane Doe"


def test_update_user_partial(service, existing_user):
    updated = service.update_user(existing_user.id, email="new@example.com")

    assert updated.username == "johndoe"  # unchanged
    assert updated.email == "new@example.com"


def test_update_user_not_found(service):
    assert service.update_user(999, username="x") is None


def test_delete_user(service, existing_user):
    result = service.delete_user(existing_user.id)

    assert result is True
    assert service.get_user(existing_user.id) is None


def test_delete_user_not_found(service):
    assert service.delete_user(999) is False
