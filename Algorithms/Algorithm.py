from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def execute(self):
        pass
