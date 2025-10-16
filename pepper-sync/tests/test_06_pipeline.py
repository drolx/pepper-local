import pytest


@pytest.fixture
def instance():
    return False


def test_init(instance):
    assert instance == True
