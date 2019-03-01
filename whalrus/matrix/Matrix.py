import logging
import numpy as np
import pandas as pd
from whalrus.utils.Utils import DeleteCacheMixin, cached_property, NiceSet, set_to_list
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class Matrix(DeleteCacheMixin):
    """
    A way to compute a matrix from a profile.

    :param ballots: if mentioned, will be passed to `__call__` immediately after initialization.
    :param weights: if mentioned, will be passed to `__call__` immediately after initialization.
    :param voters: if mentioned, will be passed to `__call__` immediately after initialization.
    :param candidates: if mentioned, will be passed to `__call__` immediately after initialization.
    :param converter: if mentioned, will be passed to `__call__` immediately after initialization.
    :param default_converter: the default converter that is used to convert input ballots. This converter is
        used when no converter is explicitly given to `__call__`.

    A :class:`Matrix` object is a callable whose inputs are ballots and optionally weights, voters, candidates and a
    converter. When it is called, it loads the profile. The output of the call is the :class:`Matrix` object itself.
    But after the call, you can access to the computed variables (ending with an underscore), such as
    :attr:`data_`.

    At the initialization of a :class:`Matrix` object, some options can be given, such as a default converter. In
    some subclasses, there can also be other options.

    Cf. :class:`MatrixWeightedMajority` for some examples.

    Remark: this `__init__` must always be called at the end of the subclasses' `__init__`.
    """

    def __init__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None,
                 default_converter: ConverterBallot=ConverterBallotGeneral()):
        # Parameters
        self.default_converter = default_converter
        # Computed variables
        self.profile_ = None
        self.profile_converted_ = None
        self.candidates_ = None
        # Optional: load a profile at initialization
        if ballots is not None:
            self(ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter)

    def __call__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None):
        self.profile_ = Profile(ballots, weights=weights, voters=voters)
        if converter is None:
            converter = self.default_converter
        self.profile_converted_ = Profile([converter(b, candidates) for b in self.profile_],
                                          weights=self.profile_.weights, voters=self.profile_.voters)
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
    def as_dict_(self) -> dict:
        """
        The matrix, as a dictionary.

        :return: a dictionary. Keys are pairs of candidates, and values are the coefficients of the matrix.
        """
        raise NotImplementedError

    @cached_property
    def as_array_(self) -> np.array:
        """
        The matrix, as a numpy array.

        :return: a numpy array. Each row and each column corresponds to a candidate (candidates are sorted if
            possible).
        """
        candidates_as_list = set_to_list(self.candidates_)
        return np.array([[self.as_dict_[(c, d)] for d in candidates_as_list] for c in candidates_as_list])

    @cached_property
    def as_df_(self) -> pd.DataFrame:
        """
        The matrix, as a pandas dataframe.

        :return: a pandas dataframe, whose rows and columns represent the candidates.
        """
        candidates_as_list = set_to_list(self.candidates_)
        return pd.DataFrame(self.as_array_, index=candidates_as_list, columns=candidates_as_list)
