from whalrus import MatrixMajority


def test():
    """
        >>> matrix = MatrixMajority(['a > b > c'])
        >>> matrix.candidates_indexes_
        {'a': 0, 'b': 1, 'c': 2}
    """
