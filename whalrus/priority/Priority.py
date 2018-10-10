import random
from typing import Sequence, Union


class Priority:
    """
    A priority setting, i.e. a policy to break ties and indifference classes.

    :param name: the name of this priority setting.

    >>> Priority.ASCENDING.choice({'c', 'a', 'b'})
    'a'
    >>> Priority.ASCENDING.sort({'c', 'a', 'b'})
    ['a', 'b', 'c']
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def choice(self, x: Sequence, reverse: bool = False) -> object:
        """
        Choose an element from a list, set, etc.

        :param x: the list, set, etc where the element is to be chosen.
        :param reverse: if False (default), then we choose the "first" or "best" element in this priority order. For
            example, if this is the ascending priority setting, we choose the lowest element. If True, then we
            choose the "last" or "worst" element. This is used, for example, in the veto rule.
        :return: the chosen element (or None). When x is empty, return None. When x has one element, return this
            element.
        """
        if len(x) == 0:
            return None
        if len(x) == 1:
            return list(x)[0]
        return self._choice(x, reverse=reverse)

    def _choice(self, x: Sequence, reverse: bool) -> object:
        """
        Auxiliary function for :meth:`choice`.

        Here, :attr:`x` is assumed to have at least 2 elements.
        """
        raise NotImplementedError

    def sort(self, x: Sequence, reverse: bool = False) -> Union[list, None]:
        """
        Sort a list, set, etc.

        :param x: the list, set, etc.
        :param reverse: if True, we use the reverse priority order.
        :return: a sorted list (or None).

        The original list :attr:`x` is not modified.
        """
        if len(x) <= 1:
            return list(x)
        return self._sort(x, reverse=reverse)

    def _sort(self, x: Sequence, reverse: bool) -> Union[list, None]:
        """
        Auxiliary function for :meth:`sort`.

        Here, :attr:`x` is assumed to have at least 2 elements.
        """
        raise NotImplementedError

    # Priority orders defined by default
    # ----------------------------------
    # The following constants are defined outside the class to avoid a problem of self-reference.

    #: When there are two elements or more, raise a ValueError.
    UNAMBIGUOUS = None
    #: When there are two elements or more, return None.
    ABSTAIN = None
    #: Ascending order (lowest is favoured).
    ASCENDING = None
    #: Descending order (highest is favoured).
    DESCENDING = None
    #: Random order.
    RANDOM = None


class PriorityUnambiguous(Priority):

    def __init__(self):
        super().__init__(name='Unambiguous')

    def __repr__(self):
        return 'Priority.UNAMBIGUOUS'

    def _choice(self, x: Sequence, reverse: bool) -> object:
        raise ValueError("Cannot choose from %r with priority set to Unambiguous." % x)

    def _sort(self, x: Sequence, reverse: bool) -> Union[list, None]:
        raise ValueError("Cannot sort %r with priority set to Unambiguous." % x)


Priority.UNAMBIGUOUS = PriorityUnambiguous()


class PriorityAbstain(Priority):

    def __init__(self):
        super().__init__(name='Abstain')

    def __repr__(self):
        return 'Priority.ABSTAIN'

    def _choice(self, x: Sequence, reverse: bool) -> object:
        return None

    def _sort(self, x: Sequence, reverse: bool) -> Union[list, None]:
        return None


Priority.ABSTAIN = PriorityAbstain()


class PriorityAscending(Priority):

    def __init__(self):
        super().__init__(name='Ascending')

    def __repr__(self):
        return 'Priority.ASCENDING'

    def _choice(self, x: Sequence, reverse: bool) -> object:
        if reverse:
            return max(x)
        return min(x)

    def _sort(self, x: Sequence, reverse: bool) -> Union[list, None]:
        return sorted(x, reverse=reverse)


Priority.ASCENDING = PriorityAscending()


class PriorityDescending(Priority):

    def __init__(self):
        super().__init__(name='Descending')

    def __repr__(self):
        return 'Priority.DESCENDING'

    def _choice(self, x: Sequence, reverse: bool) -> object:
        if reverse:
            return min(x)
        return max(x)

    def _sort(self, x: Sequence, reverse: bool) -> Union[list, None]:
        return sorted(x, reverse=not reverse)


Priority.DESCENDING = PriorityDescending()


class PriorityRandom(Priority):

    def __init__(self):
        super().__init__(name='Random')

    def __repr__(self):
        return 'Priority.RANDOM'

    def _choice(self, x: Sequence, reverse: bool) -> object:
        return random.choice(list(x))

    def _sort(self, x: Sequence, reverse: bool) -> Union[list, None]:
        return random.sample(x, len(x))


Priority.RANDOM = PriorityRandom()
