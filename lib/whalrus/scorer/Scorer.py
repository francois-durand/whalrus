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
from whalrus.ballot.Ballot import Ballot
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import DeleteCacheMixin, cached_property, NiceDict


class Scorer(DeleteCacheMixin):
    """
    A "scorer".

    :param `*args`: if present, these parameters will be passed to ``__call__`` immediately after initialization.
    :param scale: the scale in which scores are computed.
    :param `**kwargs`: if present, these parameters will be passed to ``__call__`` immediately after initialization.

    A :class:`Scorer` is a callable whose inputs are a ballot, a voter and a set of candidates (the set of candidates
    of the election).  When the scorer is called, it loads its arguments. The output of the call is the scorer
    itself. But after the call, you can access to the computed variables (ending with an underscore),
    such as :attr:`scores_`.

    At the initialization of a :class:`Scorer` object, some options can be given, such as a scale. In some
    subclasses, there can be some additional options.

    Cf. :class:`ScorerLevels` for some examples.

    :ivar ballot\_: this attribute stores the ballot given in argument of the ``__call__``.
    :ivar voter\_: this attribute stores the voter given in argument of the ``__call__``.
    :ivar candidates\_: this attribute stores the candidates given in argument of the ``__call__``.
    """

    def __init__(self, *args, scale: Scale = None, **kwargs):
        if scale is None:
            scale = Scale()
        # Parameters
        self.scale = scale
        # Computed variables
        self.ballot_ = None
        self.voter_ = None
        self.candidates_ = None
        # Optional: load a ballot at initialization
        if args or kwargs:
            self(*args, **kwargs)

    def __call__(self, ballot: Ballot, voter: object = None, candidates: set = None):
        """
        Load the arguments.

        :param ballot: a ballot. We assume that it is already in the correct subclass of :class:`Ballot` and that it is
            already restricted to the candidates of the election (if necessary).
        :param voter: the voter.
        :param candidates: the candidates.
        """
        self.ballot_ = ballot
        self.voter_ = voter
        self.candidates_ = candidates
        self.delete_cache()
        return self

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict` that, to each candidate, associates either a level in the scale or None.
            For the meaning of None, cf. :class:`RuleRangeVoting` for example. Intuitively: a score of 0 means that
            the value 0 is counted in the average, whereas None is not counted at all (i.e. the weight of the voter
            is not even counted in the denominator when computing the average).
        """
        raise NotImplementedError

    @cached_property
    def scores_as_floats_(self) -> NiceDict:
        """
        The scores, given as floats.

        :return: :attr:`scores_`, converted to floats.
        :raise ValueError: if the scores cannot be converted to floats.

        Like all conversions to floats, it is advised to use this attribute for display purposes only. For computation,
        you should always use :attr:`scores_`, which usually manipulates fractions and therefore allows for exact
        computation.
        """
        try:
            return NiceDict({c: float(v) for c, v in self.scores_.items()})
        except ValueError:
            raise ValueError('These scores cannot be converted to floats: %r.' % self.scores_)
