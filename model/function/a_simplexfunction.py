from abc import ABC, abstractmethod


class ASimplexFunction(ABC):
    @abstractmethod
    def calculate(self, left_pt, mid_pt, right_pt):
        raise NotImplementedError("Please implement the function.")