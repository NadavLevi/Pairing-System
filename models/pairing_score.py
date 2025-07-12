from dataclasses import dataclass, field
from typing import Dict

from models.provider import Provider


@dataclass(frozen=True, slots=True)
class PairingScore:
    """
    Represents a scored pairing of a provider with a consumer policy,
    including detailed component contributions.

    Attributes:
        provider (Provider): The provider that was scored.
        score (float): The total aggregated score between 0.0 and 1.0.
        components (Dict[str, float]): A breakdown of individual score components,
                                       e.g., {"stake": 0.8, "feature": 1.0, "location": 0.7}.
    """

    provider: Provider
    score: float
    components: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be a float between 0.0 and 1.0")

        if not isinstance(self.components, dict):
            raise TypeError("components must be a dictionary")

        for key, value in self.components.items():
            if not isinstance(key, str):
                raise TypeError(f"Component key '{key}' is not a string")
            if not isinstance(value, float):
                raise TypeError(f"Component value for '{key}' must be a float")
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Component score '{key}' must be between 0.0 and 1.0")
