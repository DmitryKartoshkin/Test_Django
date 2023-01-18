from rest_framework.test import APIClient
import pytest
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def data_factory():
    def factory(*args, **kwargs):
        return baker.make(*args, **kwargs)
    return factory