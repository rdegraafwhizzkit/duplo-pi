from abc import ABC, abstractmethod


class AbstractSync(ABC):

    def __init__(self, status={}):
        self.status = status
        super().__init__()

    def sync(self, color=None):
        if color is not None:
            self.status[color] = True if color not in self.status else not self.status[color]
        self.do()
        return self.status

    @abstractmethod
    def do(self):
        pass
