from abc import ABC, abstractmethod

class Frame(ABC):
    @abstractmethod
    def update(self, dt):
        pass
    @abstractmethod
    def render(self, display):
        pass