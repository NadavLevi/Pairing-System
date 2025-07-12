from functools import lru_cache
from typing import Optional, Tuple

from geopy.distance import geodesic
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

from models.policy import ConsumerPolicy
from models.provider import Provider


class LocationScore:
    _geolocator = Nominatim(user_agent="geo_locator")
    _rate_limited_geocode = RateLimiter(
        _geolocator.geocode, min_delay_seconds=1, max_retries=2
    )

    @staticmethod
    @lru_cache(maxsize=128)
    def geocode(location_str: str) -> Optional[Tuple[float, float]]:
        """
        Convert a location string into latitude and longitude coordinates.
        """
        if not location_str:
            return None
        try:
            loc = LocationScore._rate_limited_geocode(location_str)
            return (loc.latitude, loc.longitude) if loc else None
        except Exception:
            return None

    @staticmethod
    def score(provider, policy, max_distance=2000):  # max_distance in kilometers
        provider_coords = LocationScore.geocode(provider.location)
        policy_coords = LocationScore.geocode(policy.required_location)

        if not provider_coords or not policy_coords:
            return 0.0

        distance = geodesic(provider_coords, policy_coords).kilometers

        if distance == 0:
            return 1.0
        elif distance >= max_distance:
            return 0.0
        else:
            return max(0.0, 1 - (distance / max_distance))
