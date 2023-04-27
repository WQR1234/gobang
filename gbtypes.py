from enum import Enum


class Player(Enum):
    black = 1
    white = -1

    @property
    def other(self):
        if self == self.white:
            return self.black
        return self.white

    @classmethod
    def value2player(cls, v):
        if v == 1:
            return cls.black
        elif v == -1:
            return cls.white
        else:
            return None
