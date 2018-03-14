from pyparsing import Group, Word, Or, ZeroOrMore, OneOrMore, alphas, nums


def parse_weak_order(s):
    """
    Converts a string representing a weak-order to a dictionary

    Example:

    >>> s = 'Jean ~ Titi ~ tata32 > moi > toi ~ nous > eux'
    >>> parse_weak_order(s)
    {'Jean': 3, 'Titi': 3, 'tata32': 3, 'moi': 2, 'toi': 1, 'nous': 1, 'eux': 0}

    """
    candidate = Word(alphas.upper() + alphas.lower() + nums + '_')
    equiv_class = Group(candidate + ZeroOrMore(Word('~').suppress() + candidate))
    weakpref = equiv_class + OneOrMore(Word('>').suppress() + equiv_class)

    parsed = weakpref.parseString(s).asList()
    l = []

    for v, t in enumerate(reversed(parsed)):
        l = [(c, v) for c in t] + l
    return dict(l)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

