from abc import ABC, abstractmethod

current_frame = None


def set_frame(frame):
    global current_frame
    current_frame = frame


def get_frame():
    global current_frame
    return current_frame


class Frame(ABC):
    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, display):
        pass

