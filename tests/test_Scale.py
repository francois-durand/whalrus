from whalrus import Scale


def test():
    assert Scale().eq(1, 1)
    assert not Scale().eq(1, 2)

    assert not Scale().ne(1, 1)
    assert Scale().ne(1, 2)

    assert not Scale().lt(1, 1)
    assert Scale().lt(1, 2)

    assert Scale().le(1, 1)
    assert Scale().le(1, 2)

    assert not Scale().gt(1, 1)
    assert not Scale().gt(1, 2)

    assert Scale().ge(1, 1)
    assert not Scale().ge(1, 2)
