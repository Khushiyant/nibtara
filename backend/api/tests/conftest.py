import pytest
from api.models import (Judge, 
                        Lawyer, 
                        PreTrial, 
                        UserAccount)
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    return client
