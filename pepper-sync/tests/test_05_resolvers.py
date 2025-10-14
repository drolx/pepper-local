
from pepper.resolvers import ResolverState, load_resolvers
import pytest


@pytest.fixture
def instances():
    resolvers = load_resolvers()
    yield resolvers # type: ignore


def test_resolver_directions(instances):
    for res in instances:
        assert res.resolver_direction in ["in", "out"]