import pytest

from fastapi.testclient import TestClient
from tests.test import app
from scripts.lib.enums import Operation
from scripts.lib.services.math.math import show_all_operations

client = TestClient(app)

def test_show_all_operations():

    operations = show_all_operations()
    assert len(operations) == 4
    assert operations[0] == f"{Operation.ADDITION.name} ({Operation.ADDITION.value})"
