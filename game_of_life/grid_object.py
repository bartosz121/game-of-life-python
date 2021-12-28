from abc import ABC, abstractmethod


class GridObject(ABC):
    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass
