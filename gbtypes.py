from enum import Enum


class Player(Enum):
    Empty = 0
    Black = 1
    White = 2

    @property
    def other(self):
        if self == self.White:
            return self.Black
        return self.White

    # @classmethod
    # def value2player(cls, v):
    #     if v == 1:
    #         return cls.black
    #     elif v == -1:
    #         return cls.white
    #     else:
    #         return None
