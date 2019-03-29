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
import logging
import numpy as np
from whalrus.utils.Utils import DeleteCacheMixin, cached_property, NiceSet, set_to_list, NiceDict
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class Matrix(DeleteCacheMixin):
    """
    A way to compute a matrix from a profile.

    :param `*args`: if present, these parameters will be passed to ``__call__`` immediately after initialization.
    :param converter: the converter that is used to convert input ballots in order to compute
        :attr:`profile_converted_`. Default: :class:`ConverterBallotGeneral`.
    :param `**kwargs`: if present, these parameters will be passed to ``__call__`` immediately after initialization.

    A :class:`Matrix` object is a callable whose inputs are ballots and optionally weights, voters and candidates. When
    it is called, it loads the profile. The output of the call is the :class:`Matrix` object itself.
    But after the call, you can access to the computed variables (ending with an underscore), such as
    :attr:`as_dict_` or :attr:`as_array_`.

    Cf. :class:`MatrixWeightedMajority` for some examples.

    :ivar profile_original\_: the profile as it is entered by the user. This uses the constructor of :class:`Profile`.
        Hence indirectly, it uses :class:`ConverterBallotGeneral` to ensure, for example, that strings like
        ``'a > b > c'`` are converted to :class:``Ballot`` objects.
    :ivar profile_converted\_: the profile, with ballots that are adequate for the voting rule. For example,
        in :class:`MatrixWeightedMajority`, it will be :class:`BallotOrder` objects. This uses the parameter
        ``converter`` of the object.
    :ivar candidates\_: the candidates of the election, as entered in the ``__call__``.
    """

    def __init__(self, *args, converter: ConverterBallot = None, **kwargs):
        """
        Remark: this `__init__` must always be called at the end of the subclasses' `__init__`.
        """
        # Parameters
        if converter is None:
            converter = ConverterBallotGeneral()
        self.converter = converter
        # Computed variables
        self.profile_original_ = None
        self.profile_converted_ = None
        self.candidates_ = None
        # Optional: load a profile at initialization
        if args or kwargs:
            self(*args, **kwargs)

    def __call__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None):
        self.profile_original_ = Profile(ballots, weights=weights, voters=voters)
        self.profile_converted_ = Profile([self.converter(b, candidates) for b in self.profile_original_],
                                          weights=self.profile_original_.weights, voters=self.profile_original_.voters)
        if candidates is None:
            candidates = NiceSet(set().union(*[b.candidates for b in self.profile_converted_]))
        self.candidates_ = candidates
        self._check_profile(candidates)
        self.delete_cache()
        return self

    def _check_profile(self, candidates: set) -> None:
        if any([b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')

    @cached_property
    def as_dict_(self) -> NiceDict:
        """
        The matrix, as a :class:`NiceDict`.

        :return: a :class:`NiceDict`. Keys are pairs of candidates, and values are the coefficients of the matrix.
        """
        raise NotImplementedError

    @cached_property
    def candidates_as_list_(self) -> list:
        """
        The list of candidates.

        :return: a list. Candidates are sorted if possible.
        """
        return set_to_list(self.candidates_)

    @cached_property
    def candidates_indexes_(self) -> NiceDict:
        """
        The candidates as a dictionary.

        :return: a dictionary. To each candidate, it associates its index in :attr:`candidates_as_list_`.
        """
        return NiceDict({c: i for i, c in enumerate(self.candidates_as_list_)})

    @cached_property
    def as_array_(self) -> np.array:
        """
        The matrix, as a numpy array.

        :return: a numpy array. Each row and each column corresponds to a candidate (in the order of
            :attr:`candidates_as_list_`).
        """
        return np.array([[self.as_dict_[(c, d)] for d in self.candidates_as_list_] for c in self.candidates_as_list_])

    @cached_property
    def as_array_of_floats_(self) -> np.array:
        """
        The matrix, as a numpy array.

        :return: :attr:`as_array_`, converted to floats.
        """
        return self.as_array_.astype(float)
