import pytest

from models.pairing_score import PairingScore
from models.provider import Provider


@pytest.fixture
def sample_provider():
    return Provider(address="P1", stake=100, location="US", features=["f1", "f2"])


def test_valid_pairing_score(sample_provider):
    ps = PairingScore(
        provider=sample_provider,
        score=0.85,
        components={"stake": 0.9, "feature": 1.0, "location": 0.65},
    )
    assert ps.score == 0.85
    assert ps.components["stake"] == 0.9


@pytest.mark.parametrize("invalid_score", [-0.1, 1.5])
def test_score_out_of_bounds(sample_provider, invalid_score):
    with pytest.raises(ValueError, match="score must be a float between 0.0 and 1.0"):
        PairingScore(provider=sample_provider, score=invalid_score)


def test_components_not_dict(sample_provider):
    with pytest.raises(TypeError, match="components must be a dictionary"):
        PairingScore(
            provider=sample_provider, score=0.9, components=["not", "a", "dict"]
        )


def test_component_key_not_string(sample_provider):
    with pytest.raises(TypeError, match="Component key '123' is not a string"):
        PairingScore(provider=sample_provider, score=0.9, components={123: 0.5})


def test_component_value_not_float(sample_provider):
    with pytest.raises(TypeError, match="Component value for 'stake' must be a float"):
        PairingScore(provider=sample_provider, score=0.9, components={"stake": "high"})


def test_component_value_out_of_range(sample_provider):
    with pytest.raises(
        ValueError, match="Component score 'feature' must be between 0.0 and 1.0"
    ):
        PairingScore(provider=sample_provider, score=0.9, components={"feature": 1.5})
