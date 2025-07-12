from typing import List
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.extra.rate_limiter import RateLimiter
from functools import lru_cache

from filters.base_filter import BaseFilter
from models.policy import ConsumerPolicy
from models.provider import Provider


class LocationFilter(BaseFilter):
    _geolocator = Nominatim(user_agent="location_filter")
    _rate_limited_geocode = RateLimiter(_geolocator.geocode, min_delay_seconds=1)

    @staticmethod
    @lru_cache(maxsize=128)
    def geocode(location: str):
        try:
            loc = LocationFilter._rate_limited_geocode(location)
            return (loc.latitude, loc.longitude) if loc else None
        except Exception:
            return None

    def filter(
        self,
        providers: List[Provider],
        policy: ConsumerPolicy,
        strict: bool = True,
        max_distance_km: float = 2000.0
    ) -> List[Provider]:
        """
        Filters providers based on their location.

        :param providers: List of Provider objects
        :param policy: ConsumerPolicy object
        :param strict: If True, filters only exact string matches.
                       If False, includes providers within `max_distance_km`.
        :param max_distance_km: Distance threshold for flexible matching (in km)
        :return: Filtered list of Provider objects
        """
        if strict:
            return [p for p in providers if p.location == policy.required_location]

        # Flexible match: filter based on geodesic distance
        policy_coords = self.geocode(policy.required_location)
        if not policy_coords:
            return []

        filtered = []
        for provider in providers:
            provider_coords = self.geocode(provider.location)
            if provider_coords:
                distance = geodesic(provider_coords, policy_coords).kilometers
                if distance <= max_distance_km:
                    filtered.append(provider)

        return filtered