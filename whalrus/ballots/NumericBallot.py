


class NumericBallot(Ballot):
    """
    Abstract class, do not instantiate
    """

    def __init__(self, b: Dict[Any,float]):
        self.ballot = b

