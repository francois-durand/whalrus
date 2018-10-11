class ConverterBallot:
    """
    A ballot converter.

    A converter is a callable. Its input may have various formats. Its output must be a Ballot, often of a specific
    subclass.
    """

    def __call__(self, x):
        raise NotImplementedError
