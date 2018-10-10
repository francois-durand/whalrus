class Scale:
    """
    A scale used to evaluate the candidates (for range voting, approval voting, majority judgment, etc).

    This top class represents a generic scale, where two levels of the scale compare according to their internal
    methods `__lt__`, `__le__`, etc.

    For a subclass, it is sufficient to override the method :meth:`lt` and the other comparison methods will be
    modified accordingly (assuming it describes a total order).

    >>> scale = Scale()
    >>> scale.lt(1, 7)
    True
    """

    # noinspection PyMethodMayBeStatic
    def eq(self, one: object, another: object) -> bool:
        """
        Test 'equal'. Cf. :meth:`lt`.
        """
        return one == another

    # noinspection PyMethodMayBeStatic
    def ne(self, one: object, another: object) -> bool:
        """
        Test 'not equal'. Cf. :meth:`lt`.
        """
        return not self.eq(one, another)

    # noinspection PyMethodMayBeStatic
    def lt(self, one: object, another: object) -> bool:
        """
        Test 'lower than'.

        :param one: a level of the scale.
        :param another: a level of the scale.
        :return: True iff :attr:`one` is lower than :attr:`another`.

        Generally, only this method is overridden in the subclasses.
        """
        return one < another

    # noinspection PyMethodMayBeStatic
    def le(self, one: object, another: object) -> bool:
        """
        Test 'lower or equal'. Cf. :meth:`lt`.
        """
        return self.eq(one, another) or self.lt(one, another)

    # noinspection PyMethodMayBeStatic
    def gt(self, one: object, another: object) -> bool:
        """
        Test 'greater than'. Cf. :meth:`lt`.
        """
        return self.lt(another, one)

    # noinspection PyMethodMayBeStatic
    def ge(self, one: object, another: object) -> bool:
        """
        Test 'greater or equal'. Cf. :meth:`lt`.
        """
        return self.le(another, one)
