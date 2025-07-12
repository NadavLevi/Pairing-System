from typing import Union

from models.provider import Provider


class StakeScore:
    @staticmethod
    def score(provider: Provider, max_stake: Union[int, float]) -> float:
        """
        Calculate a normalized stake score between 0.0 and 1.0.

        If the provider has the maximum stake, score is 1.0.
        If stake is 0 or max_stake is 0, score is 0.0.
        Negative max_stake values are treated as invalid and return 0.0.

        :param provider: Provider instance whose stake will be scored
        :param max_stake: Maximum stake used for normalization
        :return: Normalized stake score in range [0.0, 1.0]
        """
        if not isinstance(max_stake, (int, float)) or max_stake <= 0:
            return 0.0

        score = provider.stake / max_stake
        return max(0.0, min(score, 1.0))
