import pytest

from models.policy import ConsumerPolicy


def test_valid_policy_creation():
    policy = ConsumerPolicy(
        required_location="US", required_features=["f1", "f2"], min_stake=10
    )
    assert policy.required_location == "US"
    assert policy.required_features == ["f1", "f2"]
    assert policy.min_stake == 10


@pytest.mark.parametrize("location", ["", None])
def test_invalid_required_location(location):
    with pytest.raises(
        ValueError, match="required_location must be a non-empty string"
    ):
        ConsumerPolicy(
            required_location=location, required_features=["f1"], min_stake=0
        )


@pytest.mark.parametrize("features", [None, ["f1", 123], [True], "notalist"])
def test_invalid_required_features(features):
    with pytest.raises(ValueError, match="required_features must be a list of strings"):
        ConsumerPolicy(required_location="US", required_features=features, min_stake=0)


@pytest.mark.parametrize("min_stake", [-1, -100])
def test_invalid_min_stake(min_stake):
    with pytest.raises(ValueError, match="min_stake must be a non-negative integer"):
        ConsumerPolicy(
            required_location="US", required_features=["f1"], min_stake=min_stake
        )
