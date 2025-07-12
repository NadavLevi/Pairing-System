from abc import ABC, abstractmethod

from models.policy import ConsumerPolicy
from models.provider import Provider


class BaseScore(ABC):
    @abstractmethod
    def score(self, provider: Provider, policy: ConsumerPolicy) -> float:
        """
        Calculate a normalized score for a provider based on a consumer policy.

        Subclasses must implement this method.

        :param provider: The provider to be scored
        :param policy: The consumer's policy containing scoring requirements
        :return: A float between 0.0 and 1.0 indicating how well the provider matches
        """
        pass
