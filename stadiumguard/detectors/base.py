from abc import ABC, abstractmethod


class Detector(ABC):
    @abstractmethod
    def update(self, frame, people):
        ...
        