import pytest

from filters.feature_filter import FeatureFilter
from filters.location_filter import LocationFilter
from filters.stake_filter import StakeFilter
from models.policy import ConsumerPolicy
from models.provider import Provider


@pytest.fixture
def sample_providers():
    return [
        Provider(address="A1", stake=100, location="US", features=["f1", "f2"]),
        Provider(address="A2", stake=50, location="EU", features=["f2"]),
        Provider(address="A3", stake=10, location="US", features=[]),
    ]


@pytest.fixture
def default_policy():
    return ConsumerPolicy(
        required_location="US", required_features=["f1"], min_stake=20
    )


@pytest.mark.parametrize(
    "filter_cls, expected_addresses",
    [
        (LocationFilter, {"A1", "A3"}),  # providers in US
        (FeatureFilter, {"A1"}),  # only A1 has 'f1'
        (StakeFilter, {"A1", "A2"}),  # stake >= 20
    ],
)
def test_filters_return_expected_results(
    filter_cls, sample_providers, default_policy, expected_addresses
):
    filtered = filter_cls().filter(sample_providers, default_policy)
    result_addresses = {p.address for p in filtered}
    assert result_addresses == expected_addresses, f"{filter_cls.__name__} failed"


@pytest.mark.xfail(
    reason="Only 2 providers match US location, this test incorrectly expects 3"
)
def test_location_filter_incorrect_expectation(sample_providers, default_policy):
    result = LocationFilter().filter(sample_providers, default_policy)
    assert len(result) == 3  # should fail (A2 is EU)


@pytest.mark.xfail(reason="FeatureFilter should exclude providers lacking 'f1'")
def test_feature_filter_incorrect_acceptance(sample_providers, default_policy):
    filtered = FeatureFilter().filter(sample_providers, default_policy)
    for p in filtered:
        assert "f1" not in p.features  # intentionally wrong logic


@pytest.mark.xfail(
    reason="No provider has stake >= 200, expecting 1 to demonstrate failure"
)
def test_stake_filter_high_threshold_fails(sample_providers):
    strict_policy = ConsumerPolicy(
        required_location="US", required_features=["f1"], min_stake=200
    )
    result = StakeFilter().filter(sample_providers, strict_policy)
    assert len(result) == 1  # should fail, none meet the requirement
