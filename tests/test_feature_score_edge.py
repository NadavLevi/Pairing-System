import pytest

from models.policy import ConsumerPolicy
from models.provider import Provider
from scoring.feature_score import FeatureScore


def test_feature_score_value_error():
    provider = Provider("X", 100, "US", ["f1"])
    policy = ConsumerPolicy("US", ["f1"], 0)
    with pytest.raises(ValueError):
        FeatureScore.score(provider, policy, max_features=0)
