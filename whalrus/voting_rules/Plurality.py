import VotingRule

class Plurality(VotingRule):

    def __init__(self):
        super().__init__()
        return self

    @lru_cache(maxsize=1)
    def scores(self):
        candidates = self.p
