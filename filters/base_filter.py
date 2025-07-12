from abc import ABC, abstractmethod
from typing import List

from models.policy import ConsumerPolicy
from models.provider import Provider


class BaseFilter(ABC):
    @abstractmethod
    def filter(
        self, providers: List[Provider], policy: ConsumerPolicy
    ) -> List[Provider]:
        """
        Filter the given list of providers based on the consumer policy.

        Must be implemented by any subclass.
        """
        pass
