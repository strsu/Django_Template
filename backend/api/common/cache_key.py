from enum import Enum


class BaseEnum(Enum):
    def __new__(cls, mean):
        obj = object.__new__(cls)
        obj._value_ = mean
        obj.mean = mean
        return obj

    def __init__(self, mean):
        self.key = self.name
        self.mean = mean

    def __str__(self):
        return self.key


class BoardCacheKey(BaseEnum):
    """
    usage : BoardCacheKey.BOARD_LIST
    """

    BOARD_LIST = "게시판 목록"
    BOARD_COUNT = "게시판 개수"
