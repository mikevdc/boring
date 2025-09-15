import pytest

from fastapi.testclient import TestClient
from tests.test import app

client = TestClient(app)

def test_get_all_users_ok(mocker):

    mock_users_list = [
        {'name': 'User 1', 'email': 'email1@gmail.com', 'created_at': '2025-09-15T20:30:00'},
        {'name': 'User 2', 'email': 'email2@proton.com', 'created_at': '2025-09-15T20:30:00'}
    ]
    mocker.patch('scripts.lib.services.users.users.UserDAO.get_all', return_value=mock_users_list)


    response = client.get("/users/all")
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, dict)
    users = users['users']

    assert len(users) > 0

    first_user = users[0]
    assert 'name' in first_user
    assert 'email' in first_user
    assert 'created_at' in first_user

    assert first_user['name'] == 'User 1'
