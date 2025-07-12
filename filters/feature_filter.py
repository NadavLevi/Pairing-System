from typing import List

from filters.base_filter import BaseFilter
from models.policy import ConsumerPolicy
from models.provider import Provider


class FeatureFilter(BaseFilter):
    def filter(
        self, providers: List[Provider], policy: ConsumerPolicy
    ) -> List[Provider]:
        return [
            p
            for p in providers
            if all(f in p.features for f in policy.required_features)
        ]
