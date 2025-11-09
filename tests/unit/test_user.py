import pytest

from app.models.user import User, pwd_context
from datetime import timedelta
import uuid

def test_hash_password():
    password = "testpassword"
    hashed = User.hash_password(password)
    assert pwd_context.verify(password, hashed)
    assert not pwd_context.verify("wrong", hashed)

def test_verify_password():
    user = User(password=User.hash_password("testpassword"))
    assert user.verify_password("testpassword")
    assert not user.verify_password("wrong")

def test_create_access_token():
    data = {"sub": str(uuid.uuid4())}
    token = User.create_access_token(data, expires_delta=timedelta(minutes=15))
    assert token

def test_verify_token():
    user_id = uuid.uuid4()
    token = User.create_access_token({"sub": str(user_id)})
    verified_id = User.verify_token(token)
    assert verified_id == user_id

    invalid_token = "invalid"
    assert User.verify_token(invalid_token) is None