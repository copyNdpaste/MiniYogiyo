import enum


class SortedBasedValue(enum.Enum):
    HIT = '-hit'
    LIKE = '-like_count'
    SCORE = '-score'

    @classmethod
    def from_str(cls, parameter):
        if parameter == 'hit':
            return cls.HIT
        elif parameter == 'like':
            return cls.LIKE
        elif parameter == 'score':
            return cls.SCORE
        else:
            raise AttributeError
