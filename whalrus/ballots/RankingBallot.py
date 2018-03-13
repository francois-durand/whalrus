



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
