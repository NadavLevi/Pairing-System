import pytest
from models.provider import Provider


def test_valid_provider_creation():
    p = Provider(address="P1", stake=100, location="US", features=["f1", "f2"])
    assert p.address == "P1"
    assert p.stake == 100
    assert p.location == "US"
    assert p.features == ["f1", "f2"]


@pytest.mark.parametrize("address", ["", None])
def test_invalid_address(address):
    with pytest.raises(ValueError, match="Provider address must be a non-empty string"):
        Provider(address=address, stake=10, location="US", features=["f1"])


@pytest.mark.parametrize("stake", [-1, -100])
def test_invalid_stake(stake):
    with pytest.raises(ValueError, match="Stake must be a non-negative integer"):
        Provider(address="P1", stake=stake, location="US", features=["f1"])


@pytest.mark.parametrize("location", ["", None])
def test_invalid_location(location):
    with pytest.raises(ValueError, match="Location must be a non-empty string"):
        Provider(address="P1", stake=10, location=location, features=["f1"])


@pytest.mark.parametrize("features", [None, ["f1", 2], [True], "notalist"])
def test_invalid_features(features):
    with pytest.raises(ValueError, match="Features must be a list of strings"):
        Provider(address="P1", stake=10, location="US", features=features)