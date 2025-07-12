import pytest

from filters.location_filter import LocationFilter
from models.policy import ConsumerPolicy
from models.provider import Provider


@pytest.fixture
def providers():
    return [
        Provider("A", 100, "New York", ["f1"]),
        Provider("B", 100, "Boston", ["f1"]),
        Provider("C", 100, "Berlin", ["f1"]),
    ]


@pytest.mark.parametrize(
    "strict,expected",
    [
        (True, ["A"]),  # only exact match
        (False, ["A", "B"]),  # close geographic match
    ],
)
def test_location_filter_modes(providers, strict, expected):
    policy = ConsumerPolicy(
        required_location="New York", required_features=["f1"], min_stake=10
    )
    filtered = LocationFilter().filter(providers, policy, strict=strict)
    addresses = [p.address for p in filtered]
    assert sorted(addresses) == sorted(expected)


def test_location_filter_no_matches():
    policy = ConsumerPolicy("Tokyo", ["f1"], 10)
    providers = [Provider("A", 100, "London", ["f1"])]
    filtered = LocationFilter().filter(providers, policy, strict=True)
    assert filtered == []
