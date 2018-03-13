


class VotingRule(LruCacheMixin):

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
