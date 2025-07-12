from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

from filters.feature_filter import FeatureFilter
from filters.location_filter import LocationFilter
from filters.stake_filter import StakeFilter
from models.pairing_score import PairingScore
from models.policy import ConsumerPolicy
from models.provider import Provider
from scoring.feature_score import FeatureScore
from scoring.location_score import LocationScore
from scoring.stake_score import StakeScore


class PairingSystem:
    def __init__(self, strict: bool = True, max_distance_km: int = 2000):
        """
        :param strict: If True, apply strict location filtering (exact match only).
        :param max_distance_km: Max geographic distance (in km) beyond which location score is 0.0
        """
        self.strict_location_match = strict
        self.max_distance_km = max_distance_km

    def filter_providers(
        self,
        providers: List[Provider],
        policy: ConsumerPolicy,
    ) -> List[Provider]:
        """
        Apply all filters to the provider list based on the consumer policy.
        """
        providers = LocationFilter().filter(
            providers, policy, self.strict_location_match, self.max_distance_km
        )
        for Filter in [FeatureFilter, StakeFilter]:
            providers = Filter().filter(providers, policy)
        return providers

    def _score_provider(
        self,
        provider: Provider,
        policy: ConsumerPolicy,
        max_stake: int,
        max_features: int,
    ) -> PairingScore:
        """
        Compute the average score of a provider.
        """
        stake_score = StakeScore.score(provider, max_stake)
        feature_score = FeatureScore.score(provider, policy, max_features)
        location_score = LocationScore.score(
            provider, policy, max_distance=self.max_distance_km
        )

        average_score = (stake_score + feature_score + location_score) / 3
        return PairingScore(
            provider=provider,
            score=average_score,
            components={
                "stake_score": stake_score,
                "feature_score": feature_score,
                "location_score": location_score,
            },
        )

    def rank_providers(
        self, providers: List[Provider], policy: ConsumerPolicy
    ) -> List[PairingScore]:
        """
        Score and sort providers by their average score (descending).
        """
        max_stake = max((p.stake for p in providers), default=1)
        max_features = max((len(p.features) for p in providers), default=1)
        with ThreadPoolExecutor() as executor:
            return sorted(
                executor.map(
                    lambda p: self._score_provider(p, policy, max_stake, max_features),
                    providers,
                ),
                key=lambda x: x.score,
                reverse=True,
            )

    def get_pairing_list(
        self,
        providers: List[Provider],
        policy: ConsumerPolicy,
    ) -> List[PairingScore]:
        """
        Main entry point: returns the top 5 matching providers.
        """
        filtered = self.filter_providers(providers, policy)
        if not filtered:
            return []

        ranked = self.rank_providers(filtered, policy)
        return [pairing_score for pairing_score in ranked[:5]]
