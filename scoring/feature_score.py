from models.policy import ConsumerPolicy
from models.provider import Provider


from models.provider import Provider
from models.policy import ConsumerPolicy


class FeatureScore:
    @staticmethod
    def score(provider: Provider, policy: ConsumerPolicy, max_features: int) -> float:
        """
        Calculate a feature score between 0.0 and 1.0.

        - Returns 0.0 if required features are missing.
        - Otherwise returns a normalized score based on provider's total features,
          capped at 1.0 and never below 1.0 if requireds are met.

        :param provider: Provider instance
        :param policy: ConsumerPolicy specifying required_features
        :param max_features: Maximum number of features any provider has (required + extra)
        :return: A float in range [0.0, 1.0]
        """
        if max_features <= 0:
            raise ValueError("max_features must be greater than 0")

        required = set(policy.required_features)
        provider_features = set(provider.features)

        # If provider lacks any required feature, score is 0.0
        if not required.issubset(provider_features):
            return 0.0

        # Normalize total feature richness (not just extras)
        total_feature_score = len(provider_features) / max_features
        return round(min(total_feature_score, 1.0), 4)
