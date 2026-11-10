import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # The app mutates the module-level dict in place, so restore it in place too.
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
