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
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.utils.utils import cached_property, DeleteCacheMixin, convert_number
from whalrus.ballots.ballot import Ballot
from whalrus.ballots.ballot_order import BallotOrder
from typing import Union, Iterator
from numbers import Number


class Profile(DeleteCacheMixin):
    """
    A profile of ballots.

    Parameters
    ----------
    ballots : iterable
        Typically, it is a list, but it can also be a :class:`Profile`. Its elements must be :class:`Ballot` objects
        or, more generally, inputs that can be interpreted by :class:`ConverterBallotGeneral`.
    weights : list
        A list of numbers representing the weights of the ballots. Default: if :attr:`ballots` is a Profile, then use
        the weights of this profile; otherwise, all weights are 1.
    voters : list
        A list representing the voters corresponding to the ballots. Default: if :attr:`ballots` is a Profile, then use
        the voters of this profile; otherwise, all voters are None.

    Examples
    --------
    Most general syntax:

        >>> profile = Profile(
        ...     ballots=[BallotOrder('a > b ~ c'), BallotOrder('a ~ b > c')],
        ...     weights=[2, 1],
        ...     voters=['Alice', 'Bob']
        ... )
        >>> print(profile)
        Alice (2): a > b ~ c
        Bob (1): a ~ b > c

    In the following example, each ballot illustrates a different syntax:

        >>> profile = Profile([
        ...     ['a', 'b', 'c'],
        ...     ('b', 'c', 'a'),
        ...     'c > a > b',
        ... ])
        >>> print(profile)
        a > b > c
        b > c > a
        c > a > b

    Profiles have a list-like behavior in the sense that they implement ``__len__``, ``__getitem__``, ``__setitem__``
    and ``__delitem__``:

        >>> profile = Profile(['a > b', 'b > a', 'a ~ b'])
        >>> len(profile)
        3
        >>> profile[0]
        BallotOrder(['a', 'b'], candidates={'a', 'b'})
        >>> profile[0] = 'a ~ b'
        >>> print(profile)
        a ~ b
        b > a
        a ~ b
        >>> del profile[0]
        >>> print(profile)
        b > a
        a ~ b

    Profiles can be concatenated:

        >>> profile = Profile(['a > b', 'b > a']) + ['a ~ b']
        >>> print(profile)
        a > b
        b > a
        a ~ b

    Profiles can be multiplied by a scalar, which multiplies the weights:

        >>> profile = Profile(['a > b', 'b > a']) * 3
        >>> print(profile)
        (3): a > b
        (3): b > a
    """

    def __init__(self, ballots: Union[list, 'Profile'], weights: list = None, voters: list = None):
        converter = ConverterBallotGeneral()
        self._ballots = [converter(b) for b in ballots]
        if weights is None:
            if isinstance(ballots, Profile):
                weights = ballots.weights
            else:
                weights = [1] * len(ballots)
        else:
            weights = [convert_number(w) for w in weights]
        self._weights = weights
        if voters is None:
            if isinstance(ballots, Profile):
                self._voters = ballots.voters
            else:
                self._voters = [None] * len(ballots)
        else:
            self._voters = voters

    @property
    def ballots(self) -> list:
        """list of Ballot: The ballots.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile.ballots
            [BallotOrder(['a', 'b'], candidates={'a', 'b'}), BallotOrder(['b', 'a'], candidates={'a', 'b'})]
        """
        return self._ballots

    @property
    def weights(self) -> list:
        """list of Number: The weights.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile.weights
            [1, 1]
        """
        return self._weights

    @property
    def voters(self) -> list:
        """list: The voters.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'], voters=['Alice', 'Bob'])
            >>> profile.voters
            ['Alice', 'Bob']
        """
        return self._voters

    @cached_property
    def has_weights(self) -> bool:
        """bool: Presence of non-trivial weights. True iff at least one weight is not 1.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile.has_weights
            False
        """
        return any([weight != 1 for weight in self.weights])

    @cached_property
    def has_voters(self) -> bool:
        """bool: Presence of explicit voters. True iff at least one voter is not None.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile.has_voters
            False
        """
        return any([voter is not None for voter in self.voters])

    # Representation
    # ==============

    def __repr__(self) -> str:
        return 'Profile(ballots=%r, weights=%r, voters=%r)' % (self.ballots, self.weights, self.voters)

    def __str__(self) -> str:
        def i_to_str(i):
            prefix_elements = []
            if self.has_voters:
                prefix_elements.append(str(self.voters[i]))
            if self.has_weights:
                prefix_elements.append('(' + str(self.weights[i]) + ')')
            prefix = ' '.join(prefix_elements)
            if prefix:
                prefix += ': '
            return prefix + str(self.ballots[i])

        return '\n'.join([i_to_str(i) for i in range(len(self.ballots))])

    # List-like behavior
    # ==================

    def append(self, ballot: object, weight: Number=1, voter: object=None) -> None:
        """
        Append a ballot to the profile.

        Parameters
        ----------
        ballot : object
            A ballot or, more generally, an input that can be interpreted by :class:`ConverterBallotGeneral`.
        weight : Number
            The weight of the ballot.
        voter : object
            The voter.

        Examples
        --------
            >>> profile = Profile(['a > b'])
            >>> profile.append('b > a')
            >>> print(profile)
            a > b
            b > a
        """
        self._ballots.append(ConverterBallotGeneral()(ballot))
        self._weights.append(convert_number(weight))
        self._voters.append(voter)
        self.delete_cache()

    def remove(self, ballot: object=None, voter: object=None) -> None:
        """
        Remove a ballot from the profile.

        If only the ballot is specified, remove the first matching ballot in the profile.
        If only the voter is specified, remove the first ballot whose voter matches the given voter.
        If both are specified, remove the first ballot matching both descriptions.

        Parameters
        ----------
        ballot : object
            The ballot or, more generally, an input that can be interpreted by :class:`ConverterBallotGeneral`.
        voter : object
            The voter.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile.remove('b > a')
            >>> print(profile)
            a > b
        """
        if ballot is None:
            i = next(i for i, v in enumerate(self.voters) if v == voter)
        elif voter is None:
            i = next(i for i, b in enumerate(self.ballots) if b == ConverterBallotGeneral()(ballot))
        else:
            i = next(i for i, b in enumerate(self.ballots)
                     if b == ConverterBallotGeneral()(ballot) and self.voters[i] == voter)
        del self._ballots[i]
        del self._voters[i]
        del self._weights[i]
        self.delete_cache()

    def __len__(self) -> int:
        """int: Length. The number of ballots in the profile.

        Examples
        --------
            >>> profile = Profile(['a > b', 'a > b', 'b > a'])
            >>> len(profile)
            3
        """
        return len(self.ballots)

    def __getitem__(self, item: int) -> Ballot:
        """Get.

        Parameters
        ----------
        item : int

        Returns
        -------
        Ballot
            The corresponding ballot (this function does not return the weight or the voter).

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile[0]
            BallotOrder(['a', 'b'], candidates={'a', 'b'})
        """
        return self.ballots[item]

    def __setitem__(self, key: int, value: object) -> None:
        """Set.

        Set the corresponding ballot (it does not change the weight or the voter).

        Parameters
        ----------
        key : int
        value : object
            The new ballot or, more generally, an input that is understandable by a :class:`ConverterBallotGeneral`.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile[0] = 'a ~ b'
            >>> print(profile)
            a ~ b
            b > a
        """
        self._ballots[key] = ConverterBallotGeneral()(value)
        self.delete_cache()

    def __delitem__(self, key: int) -> None:
        """
        Delete.

        Delete the corresponding ballot.

        Parameters
        ----------
        key : int

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> del profile[0]
            >>> print(profile)
            b > a
        """
        del self._ballots[key]
        del self._weights[key]
        del self._voters[key]
        self.delete_cache()

    # Dict-like behavior
    def items(self) -> Iterator:
        """
        Items of the profile.

        Returns
        -------
        Iterator
            A zip of triples (ballot, weight, voter).

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> for ballot, weight, voter in profile.items():
            ...     print('Ballot %s, weight %s, voter %s.' % (ballot, weight, voter))
            Ballot a > b, weight 1, voter None.
            Ballot b > a, weight 1, voter None.
        """
        return zip(self.ballots, self.weights, self.voters)

    # Some basic operations
    # =====================

    def __add__(self, other: Union['Profile', list]) -> 'Profile':
        """
        Concatenate with another profile.

        Parameters
        ----------
        other : Profile or list
            Another Profile (or a list of ballots).

        Returns
        -------
        Profile
            This profile, followed by the other profile.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> profile2 = Profile(['a ~ b'])
            >>> print(profile + profile2)
            a > b
            b > a
            a ~ b
        """
        if isinstance(other, list):
            other = Profile(other)
        return Profile(ballots=self.ballots + other.ballots, weights=self.weights + other.weights,
                       voters=self.voters + other.voters)

    def __mul__(self, other: Number) -> 'Profile':
        """
        Multiply the weights.

        Parameters
        ----------
        other : Number

        Returns
        -------
        Profile
            This profile, with weights multiplied by the number.

        Examples
        --------
            >>> profile = Profile(['a > b', 'b > a'])
            >>> print(profile * 3)
            (3): a > b
            (3): b > a
        """
        other = convert_number(other)
        return Profile(ballots=self.ballots, weights=[convert_number(w * other) for w in self.weights],
                       voters=self.voters)
