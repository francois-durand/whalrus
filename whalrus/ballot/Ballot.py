# -*- coding: utf-8 -*-
"""
Copyright Sylvain Bouveret, Yann Chevaleyre and François Durand
sylvain.bouveret@imag.fr, yann.chevaleyre@dauphine.fr, fradurand@gmail.com

This file is part of Whalrus.

Whalrus is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Whalrus is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Whalrus.  If not, see <http://www.gnu.org/licenses/>.
"""
from whalrus.utils.Utils import NiceSet


class Ballot:
    """
    A ballot.

    The philosophy of this class is to stick as much as possible to the message that the voter emitted, in the
    context where she emitted it. For example, consider a range voting setting with candidates `a`, `b`, `c`
    and a scale of grades from 0 to 100. If the voter emits a ballot where `a` has grade 60 and `b` has grade 30, then
    the :class:`Ballot` object simply records all this: what candidates were present, what was the scale of authorized
    grades, and what the voter indicated in her ballot. But, for example:

    * It makes no assumption whether the voter prefers `a` to `c`. Maybe she did not mention `c` because she didn't
      like it, maybe because she didn't know it.
    * It makes no assumption about what would be the voter's ballot with a scale from 0 to 10. Maybe it would be
      ``{'a': 6, 'b': 3}``, maybe not.

    Ballot converters (cf. :class:`ConverterBallot`) will be used each time we need an information that is beyond
    what the ballot clearly indicated.
    """

    @property
    def candidates(self) -> NiceSet:
        """
        The candidates that were available at the moment when the voter cast her ballot.

        :return: a :class:`NiceSet`. As a consequence, candidates must be hashable objects.
        """
        raise NotImplementedError

    def first(self, candidates: set = None, **kwargs) -> object:
        """
        The first (= most liked) candidate. Implementation is optional.

        :param candidates: a set of candidates (it can be any set of candidates, not necessarily a subset of
            ``self.candidates``). Default: ``self.candidates``.
        :param kwargs: some options (depending on the subclass).
        :return: the first (= most liked) candidate, chosen in the intersection of ``self.candidates`` and the argument
            ``candidates``. Can return None for an "abstention".

        Typical example: the ballot was cast in a context where candidates `a`, `b`, `c`, `d` were declared. Hence
        ``self.candidates == {'a', 'b', 'c', 'd'}``. Later, candidate `a` is removed from the election. Then we can
        use this method with the optional argument ``candidates = {'b', 'c', 'd'}`` to know who is the most liked
        candidate of the voter in this new context.

        In most subclasses, this method needs some options (``kwargs``) to solve ambiguities in this conversion. In
        some other subclasses, this method may even stay unimplemented.
        """
        raise NotImplementedError

    def last(self, candidates: set=None, **kwargs) -> object:
        """
        The last (= most disliked) candidate. Implementation is optional.

        :param candidates: a set of candidates (it can be any set of candidates, not necessarily a subset of
            ``self.candidates``). Default: ``self.candidates``.
        :param kwargs: some options (depending on the subclass).
        :return: the last (= most disliked) candidate, chosen in the intersection of ``self.candidates`` and the
            argument ``candidates``. Can return None for an "abstention".

        Cf. :meth:`first` for more information.
        """
        raise NotImplementedError

    def restrict(self, candidates=None, **kwargs) -> 'Ballot':
        """
        Restrict the ballot to less candidates. Implementation is optional.

        :param candidates: a set of candidates (it can be any set of candidates, not necessarily a subset of
            ``self.candidates``). Default: ``self.candidates``.
        :param kwargs: some options (depending of the subclass).
        :return: the same ballot, "restricted" to the candidates given.

        Additional candidates (that are in the argument ``candidates`` but not in ``self.candidates``) are generally not
        taken into account in the restricted ballot. For example, in a election with candidates `a`, `b`, `c`, assume
        that the voter emits an ordered ballot ``a > b > c``. Later, candidate `a` is removed and candidate `d` is
        added. Then the "restricted" ballot to ``{'b, 'c', 'd'}`` is ``b > c``. For more details, see for example
        :meth:`BallotOrder.restrict`.
        """
        raise NotImplementedError
