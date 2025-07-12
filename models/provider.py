from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True, slots=True)
class Provider:
    address: str
    stake: int
    location: str
    features: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.address or not isinstance(self.address, str):
            raise ValueError("Provider address must be a non-empty string")

        if self.stake < 0:
            raise ValueError("Stake must be a non-negative integer")

        if not self.location or not isinstance(self.location, str):
            raise ValueError("Location must be a non-empty string")

        if not isinstance(self.features, list) or not all(
            isinstance(f, str) for f in self.features
        ):
            raise ValueError("Features must be a list of strings")
