import pytest

from fastapi.testclient import TestClient
from tests.test import app
from scripts.lib.enums import Operation
from scripts.lib.services.users.users import show_all_users

client = TestClient(app)

def test_show_all_users(mocker):

    mock_users_list = [
        {'name': 'User 1', 'email': 'email1@gmail.com', 'created_at': '2025-09-15T20:30:00'},
        {'name': 'User 2', 'email': 'email2@proton.com', 'created_at': '2025-09-15T20:30:00'}
    ]
    mocker.patch('scripts.lib.services.users.users.UserDAO.get_all', return_value=mock_users_list)

    users = show_all_users()
    assert len(users) == 2
    assert users[0]['name'] == 'User 1'
    assert users[1]['email'] == 'email2@proton.com'
