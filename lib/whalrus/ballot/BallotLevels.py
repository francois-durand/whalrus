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
import numbers
from typing import KeysView, ValuesView, ItemsView
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.scale.Scale import Scale
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.utils.Utils import cached_property, dict_to_items, NiceSet, NiceDict, convert_number


class BallotLevels(BallotOrder):
    # noinspection PyRedeclaration
    """
    Ballot with an evaluation of the candidates.

    :param b: a dictionary whose keys are candidates and whose values represent some form of evaluation. The keys and
        the values must be hashable.
    :param candidates: the candidates that were available at the moment when the voter cast her ballot. Default:
        candidates that are explicitly mentioned in the ballot :attr:`b`.
    :param scale: the authorized scale of evaluations at the moment when the voter cast her ballot.
        Default: ``Scale()`` (meaning in this case "unknown").

    Most general syntax:

    >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3},
    ...                       candidates={'a', 'b', 'c', 'd', 'e'},
    ...                       scale=ScaleRange(low=0, high=10))

    Other examples of syntax:

    >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3})
    >>> ballot = BallotLevels({'a': 'Good', 'b': 'Bad', 'c': 'Bad'},
    ...                       scale=ScaleFromList(['Bad', 'Medium', 'Good']))

    In addition to the set-like and list-like behaviors defined in parent class :class:`BallotOrder`, it also has
    a dictionary-like behavior in the sense that it implements ``__getitem__``:

    >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3})
    >>> ballot['a']
    10
    """

    # Core features: ballot and candidates
    # ====================================

    def __init__(self, b: dict, candidates: set=None, scale: Scale=None):
        if scale is None:
            scale = Scale()
        self.scale = scale
        super().__init__(b, candidates)

    def _parse(self, b: dict) -> None:
        """
        For this subclass, the internal representation is of the form {'a': 10, 'b': 7, 'c': 3}, meaning
        that a has evaluation 10; b, 7; and c, 3.

        :param b: a dictionary.
        """
        self._internal_representation = NiceDict({c: convert_number(v) for c, v in b.items()})

    @cached_property
    def as_dict(self) -> NiceDict:
        """
        Dictionary format.

        :return: a :class:`NiceDict`, whose keys are candidates and values are levels of evaluation.

        >>> BallotLevels({'a': 10, 'b': 7, 'c': 3}).as_dict
        {'a': 10, 'b': 7, 'c': 3}
        """
        return self._internal_representation

    @cached_property
    def as_weak_order(self) -> list:
        return [NiceSet(k for k in self.as_dict.keys() if self.as_dict[k] == v)
                for v in sorted(set(self.as_dict.values()), reverse=True)]

    @cached_property
    def candidates_in_b(self) -> NiceSet:
        return NiceSet(self.as_dict.keys())

    @cached_property
    def is_numeric(self):
        return all([isinstance(v, numbers.Number) for k, v in self.items()])

    # Representation
    # ==============

    def __repr__(self) -> str:
        return 'BallotLevels(%s, candidates=%s, scale=%s)' % (
            self.as_dict, self.candidates, repr(self.scale)
        )

    def __str__(self) -> str:
        return ', '.join([str(k) + ': ' + str(v) for k, v in dict_to_items(self.as_dict)])

    # Restrict the ballot
    # ===================

    def restrict(self, candidates: set=None, **kwargs) -> 'BallotLevels':
        if kwargs:
            raise TypeError("restrict() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        if candidates is None:
            return self
        return BallotLevels({k: v for k, v in self.as_dict.items() if k in candidates},
                            candidates=NiceSet(self.candidates & candidates), scale=self.scale)

    # Dictionary behavior
    # ===================

    def __getitem__(self, item: object) -> object:
        """
        Get an evaluation.

        :param item: a candidate.
        :return: the evaluation for this candidate.

        >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3})
        >>> ballot['a']
        10
        """
        return self.as_dict[item]

    def keys(self) -> KeysView:
        """
        Keys of the ballot.

        :return: This is a shortcut for ``self.as_dict.keys()``.

        >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3}, candidates={'a', 'b', 'c', 'd', 'e'})
        >>> sorted(ballot.keys())
        ['a', 'b', 'c']
        """
        return self.as_dict.keys()

    def values(self) -> ValuesView:
        """
        Values of the ballot.

        :return: This is a shortcut for ``self.as_dict.values()``.

        >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3}, candidates={'a', 'b', 'c', 'd', 'e'})
        >>> sorted(ballot.values())
        [3, 7, 10]
        """
        return self.as_dict.values()

    def items(self) -> ItemsView:
        """
        Items of the ballot.

        :return: this is a shortcut for ``self.as_dict.items()``.

        >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 3}, candidates={'a', 'b', 'c', 'd', 'e'})
        >>> sorted(ballot.items())
        [('a', 10), ('b', 7), ('c', 3)]
        """
        return self.as_dict.items()
