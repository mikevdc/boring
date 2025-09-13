import pytest

from fastapi.testclient import TestClient
from tests.test import app

client = TestClient(app)

def test_get_all_operations_ok():
    response = client.get("/maths/all")
    assert response.status_code == 200
    assert response.json() == {
        "operations": {
            "0": "ADDITION (+)",
            "1": "SUBSTRACTION (-)",
            "2": "MULTIPLICATION (*)",
            "3": "DIVISION (/)"
        }
    }
