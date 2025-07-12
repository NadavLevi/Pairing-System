import pytest

from models.policy import ConsumerPolicy
from models.provider import Provider
from scoring.feature_score import FeatureScore
from scoring.location_score import LocationScore
from scoring.stake_score import StakeScore


@pytest.fixture
def provider_set():
    return [
        Provider("A", 100, "US", ["f1", "f2"]),
        Provider("B", 50, "US", ["f1"]),
        Provider("C", 0, "EU", []),
    ]


@pytest.fixture
def policy():
    return ConsumerPolicy(
        required_location="US", required_features=["f1"], min_stake=10
    )


@pytest.mark.parametrize(
    "stake, max_stake, expected",
    [
        (100, 100, 1.0),
        (50, 100, 0.5),
        (0, 100, 0.0),
        (10, 0, 0.0),  # Edge: max_stake = 0
    ],
)
def test_stake_score(stake, max_stake, expected):
    provider = Provider("X", stake, "US", [])
    result = StakeScore.score(provider, max_stake)
    assert pytest.approx(result) == expected


@pytest.mark.parametrize(
    "features, required, expected",
    [
        (["f1"], ["f1"], 1.0),  # exact match for required feature
        (["f1", "f2"], ["f1"], 1.0),  # required feature + bonus feature
        (["f2"], ["f1"], 0.0),  # missing required feature
        (
            ["f1", "f2", "f3"],
            ["f1"],
            1.0,
        ),  # required feature + multiple bonus features (capped at 1.0)
        (["f1", "f2"], ["f1", "f2"], 1.0),  # all required features matched
        (["f1"], ["f1", "f2"], 0.0),  # partially matched required features
    ],
)
def test_feature_score(features, required, expected):
    """
    Test the feature scoring logic based on the updated implementation.
    """
    policy = ConsumerPolicy(
        required_location="US", required_features=required, min_stake=0
    )
    provider = Provider("X", 100, "US", features)
    result = FeatureScore.score(provider, policy, max_features=len(features))
    assert pytest.approx(result, 0.01) == expected


@pytest.mark.parametrize(
    "provider_loc, policy_loc, expected_range",
    [
        ("New York", "New York", (1.0, 1.0)),  # exact match
        ("New York", "Boston", (0.7, 0.95)),  # relatively close
        ("New York", "Berlin", (0.0, 0.1)),  # far away
        ("InvalidCity", "New York", (0.0, 0.0)),  # geocode fails
    ],
)
def test_location_score(provider_loc, policy_loc, expected_range):
    provider = Provider("X", 100, provider_loc, ["f1"])
    policy = ConsumerPolicy(policy_loc, ["f1"], 10)
    result = LocationScore.score(provider, policy)
    low, high = expected_range
    assert low <= result <= high


@pytest.mark.xfail(reason="Incorrect expectation: stake is 100 but expected 0")
def test_stake_score_fail():
    provider = Provider("X", 100, "US", [])
    assert StakeScore.score(provider, 100) == 0


@pytest.mark.xfail(reason="Missing required features should give 0 score")
def test_feature_score_fail():
    policy = ConsumerPolicy("US", ["f1"], 10)
    provider = Provider("X", 100, "US", [])
    assert FeatureScore.score(provider, policy) > 0


@pytest.mark.xfail(
    reason="Provider in EU should not get perfect location score against US"
)
def test_location_score_fail():
    provider = Provider("X", 100, "Berlin", ["f1"])
    policy = ConsumerPolicy("New York", ["f1"], 10)
    assert LocationScore.score(provider, policy) == 1.0


def test_feature_score_multiple_providers(provider_set):
    """
    Test feature scoring across multiple providers with a policy requiring two features.
    """
    policy = ConsumerPolicy(
        required_location="US", required_features=["f1"], min_stake=0
    )
    expected = [1.0, 0.5, 0.0]
    max_features = max(len(p.features) for p in provider_set)
    results = [FeatureScore.score(p, policy, max_features) for p in provider_set]
    assert pytest.approx(results, 0.01) == expected
