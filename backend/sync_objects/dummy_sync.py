from .abstract_sync import AbstractSync
from pprint import pprint as pp


class DummySync(AbstractSync):
    def do(self):
        pp(self.status)
