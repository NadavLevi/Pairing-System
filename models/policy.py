from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True, slots=True)
class ConsumerPolicy:
    required_location: str
    required_features: List[str] = field(default_factory=list)
    min_stake: int = 0

    def __post_init__(self):
        if not self.required_location or not isinstance(self.required_location, str):
            raise ValueError("required_location must be a non-empty string")

        if not isinstance(self.required_features, list) or not all(
            isinstance(f, str) for f in self.required_features
        ):
            raise ValueError("required_features must be a list of strings")

        if self.min_stake < 0:
            raise ValueError("min_stake must be a non-negative integer")
