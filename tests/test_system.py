import pytest

from models.policy import ConsumerPolicy
from models.provider import Provider
from pairing_system.system import PairingSystem


@pytest.fixture
def providers():
    return [
        Provider("A", 100, "US", ["f1", "f2"]),
        Provider("B", 50, "US", ["f1"]),
        Provider("C", 200, "DE", ["f1", "f2", "f3"]),
        Provider("D", 80, "US", ["f1", "f3"]),
        Provider("E", 120, "US", ["f1"]),
    ]


@pytest.fixture
def policy():
    return ConsumerPolicy(
        required_location="US", required_features=["f1"], min_stake=60
    )


def test_filter_providers_returns_expected(providers, policy):
    system = PairingSystem()
    filtered = system.filter_providers(providers, policy)
    expected_addresses = {"A", "D", "E"}
    actual_addresses = {p.address for p in filtered}
    assert actual_addresses == expected_addresses
    assert len(filtered) == 3


def test_rank_providers_order_is_correct(providers, policy):
    system = PairingSystem()
    filtered = system.filter_providers(providers, policy)
    ranked = system.rank_providers(filtered, policy)
    ranked_providers = [p.provider for p in ranked]
    ranked_addresses = [p.address for p in ranked_providers]

    # Score depends on stake (normalized), feature match, and location
    expected_order = ["A", "D", "E"]  # Assuming stake: A > D > E
    assert ranked_addresses == expected_order


def test_get_pairing_list_matches_expected(providers, policy):
    system = PairingSystem()
    top_pairs = system.get_pairing_list(providers, policy)
    top_providers = [p.provider for p in top_pairs]
    top_addresses = [p.address for p in top_providers]
    assert top_addresses == ["A", "D", "E"]
    assert len(top_addresses) <= 5


@pytest.mark.xfail(
    reason="Expecting E first, but A has higher stake and should be first"
)
def test_pairing_list_incorrect_order_expectation(providers, policy):
    system = PairingSystem()
    result = system.get_pairing_list(providers, policy)
    assert result[0].provider.address == "E"  # Should actually be "A"


@pytest.mark.xfail(reason="Expecting one too many providers (should be 3)")
def test_filter_returns_too_many(providers, policy):
    system = PairingSystem()
    filtered = system.filter_providers(providers, policy)
    assert len(filtered) == 4
