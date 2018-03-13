import numpy as np
from collections import Iterable

class Ballot(object):
    pass


class NumericBallot(Ballot):
    """
    Abstract class, do not instantiate
    """

    def __init__(self, b):
        self.ballot = b


class GradeBallot(NumericBallot):
    def __init__(self, b):
        """
        myBallot = GradeBallot({'jean':23,'pie':12})
        """
        super().__init__(b)


class RankingBallot(NumericBallot):
    def __init__(self, b):
        """
        myBallot = RankingBallot(['jean','pie'])
        """
        if type(b) == dict:
            super().__init__(b)

        elif type(b) in [list,tuple,set]:  # changer en iterable
            super().__init__( {x: i for i, x in enumerate(reversed(list(b)))} )

        else:
            raise TypeError('expecting dict,list,tuple or set')

######################################

class VotingRule(EmptyLruCacheMixin):

    def __init__(self):
        raise NotImplementedError()

    def load_profile(self, p):
        self.p = p
        self.empty_lru_caches()

    def winner(self):
        raise NotImplemented

    def cowinners(self):
        raise NotImplemented

    def scores(self):
        raise NotImplemented

    def winner_ranking(self):
        raise NotImplemented


######################################


from functools import lru_cache


class EmptyLruCacheMixin(object):
    def empty_lru_caches(self):
        """
        """
        for field in dir(self):
            f = getattr(self, field)
            if callable(f) and hasattr(f, 'cache_info'):
                f.cache_clear()


class TestEmptyLruCacheMixin(EmptyLruCacheMixin):
    def __init__(self):
        assert tuple(self.g.cache_info()) == (0, 0, 1, 0)
        self.g(3)
        assert tuple(self.g.cache_info()) == (0, 1, 1, 1)
        self.empty_lru_caches()
        assert tuple(self.g.cache_info()) == (0, 0, 1, 0)

    @lru_cache(maxsize=1)
    def g(self, n):
        return n * n

    def h(self):
        print('h')


t = TestEmptyLruCacheMixin()
