import pytest
import sys

from loguru import logger
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.resolve()))

@pytest.fixture(autouse=True)
def silence_loguru():
    logger.remove()
    logger.add(lambda _: None)