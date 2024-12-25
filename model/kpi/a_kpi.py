from abc import ABC, abstractmethod


class AKPI(ABC):
    @abstractmethod
    def calculate(self, *args):
        raise NotImplementedError("Please implement a KPI calculation.")