
import numpy as np


class Ballot(object):
    pass

class NumericBallot(Ballot):
    """
    Abstract class, do not instantiate
    """
    def __init__(self ,b):
        self.ballot = b


class GradeBallot(NumericBallot):
    def __init__(self ,b):
        """
        myBallot = GradeBallot({'jean':23,'pie':12})
        """
        super().__init__(b)



class RankingBallot(NumericBallot):
    def __init__(self ,b):
        """
        myBallot = RankingBallot(['jean','pie'])
        """
        if type(b) == dict:
            super().__init__(b)
        elif type(b) == list: # changer en iterable
            super().__init__( {x :i for i ,x in enumerate(reversed(list(b)))} )



######################################

class VotingRule(object):
    def __init__(self):
        raise NotImplementedError()

def load_profile(self ,p):
    self.p = p

def winner(self):
    if not hasattr(self ,'_winner'):
        self._compute_winner()
    return getattr(self ,'_winner')

def _compute_winner(self):
    """
    Assigns a value to self._winner
    """
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
            if callable(f) and hasattr(f,'cache_info'):
                f.cache_clear()



class TestEmptyLruCacheMixin(EmptyLruCacheMixin):
    def __init__(self):
        assert tuple(self.g.cache_info()) == (0,0,1,0)
        self.g(3)
        assert tuple(self.g.cache_info()) == (0,1,1,1)
        self.empty_lru_caches()
        assert tuple(self.g.cache_info()) == (0,0,1,0)

    @lru_cache(maxsize=1)
    def g(self,n):
        return n*n

    def h(self):
        print('h')


t = TestEmptyLruCacheMixin()

