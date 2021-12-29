from app.users.models import User
from app import db
import pytest


@pytest.fixture(scope="module")
def setup():
    # setup
    session = db.get_session()
    yield session
    # teardown
    q = User.objects.filter(email="test@test.com")
    if q.count() != 0:
        q.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email='test@test.com', password='test123')


def test_duplicate_user(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test.com', password='test123')


def test_invalid_email(setup):
    with pytest.raises(Exception):
        User.create_user(email='test@test', password='test123')


def test_valid_password(setup):
    q = User.objects.filter(email="test@test.com")
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password("test123") == True
    assert user_obj.verify_password("test12345") == False
