from whalrus.utils.Utils import cached_property
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.profile.Profile import Profile
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union
from whalrus.matrix.Matrix import Matrix


class MatrixWeightedMajority(Matrix):
    """
    The weighted majority matrix.

    :param higher_vs_lower: number of points for candidate ``c`` when it is ordered higher than candidate ``d``.
    :param lower_vs_higher: number of points for candidate ``c`` when it is ordered lower than candidate ``d``.
    :param indifference: number of points for candidate ``c`` when it is ordered the same as candidate ``d``.
    :param ordered_vs_unordered: number of points for candidate ``c`` when it is ordered and ``d`` is unordered.
    :param unordered_vs_ordered: number of points for candidate ``c`` when it is unordered and ``d`` is ordered.
    :param unordered_vs_unordered: number of points for candidate ``c`` when it is unordered and ``d`` is unordered.
    :param ordered_vs_absent: number of points for candidate ``c`` when it ordered and ``d`` is absent.
    :param absent_vs_ordered: number of points for candidate ``c`` when it absent and ``d`` is ordered.
    :param unordered_vs_absent: number of points for candidate ``c`` when it unordered and ``d`` is absent.
    :param absent_vs_unordered: number of points for candidate ``c`` when it absent and ``d`` is unordered.
    :param absent_vs_absent: number of points for candidate ``c`` when it absent and ``d`` is absent.
    :param default_score: default score in the matrix in case of division by 0.

    An 'unordered' candidate is a candidate that the voter has seen but not included in her ranking; i.e. it is in the
    attribute :attr:`candidates_not_in_b` of the ballot. An 'absent' candidate is a candidate that the voter has not
    even seen; i.e. it is in ``self.candidates_``, but not the attribute :attr:`candidates` of the ballot.

    For all the parameters above, the value None can be used. In that case, the corresponding occurrences are not
    taken into account in the average (neither the numerator, not the denominator). Cf. examples below.

    Basic usage:

    >>> ballot = BallotOrder('a > b ~ c', candidates={'a', 'b', 'c', 'd', 'e'})
    >>> MatrixWeightedMajority(ballots=[ballot]).as_df_
         a    b    c    d    e
    a  0.0  1.0  1.0  1.0  1.0
    b  0.0  0.0  0.5  1.0  1.0
    c  0.0  0.5  0.0  1.0  1.0
    d  0.0  0.0  0.0  0.0  0.5
    e  0.0  0.0  0.0  0.5  0.0

    In the most general syntax, firstly, you define the matrix computation algorithm:

    >>> matrix = MatrixWeightedMajority(indifference=None)

    Secondly, you use it as a callable to load a particular election (profile, candidates):

    >>> matrix(ballots=['a > b', 'a ~ b'], weights=[2, 1], voters=['Alice', 'Bob'], candidates={'a', 'b'})  # doctest:+ELLIPSIS
    <MatrixWeightedMajority.MatrixWeightedMajority object at ...>

    Finally, you can access the computed variables:

    >>> matrix.as_array_
    array([[0., 1.],
           [0., 0.]])
    >>> matrix.as_df_
         a    b
    a  0.0  1.0
    b  0.0  0.0

    Later, if you wish, you can load another profile with the same matrix computation algorithm, and so on.

    Using the options:

    >>> # With ``indifference = .5`` (default), the ratio of voters who like ``a`` better than ``b`` is 1.5 / 2 = 0.75
    >>> # (the indifferent voter gives .5 point and is counted in the denominator):
    >>> MatrixWeightedMajority(['a > b', 'a ~ b']).as_df_
          a     b
    a  0.00  0.75
    b  0.25  0.00
    >>> # With ``indifference = 0.``, the ratio of voters who like ``a`` better than ``b`` is 1. / 2 = 0.5
    >>> # (the indifferent voter gives no point, but is counted in the denominator):
    >>> MatrixWeightedMajority(['a > b', 'a ~ b'], indifference=0.).as_df_
         a    b
    a  0.0  0.5
    b  0.0  0.0
    >>> # With ``indifference = None``, the ratio of voters who like ``a`` better than ``b`` is 1. / 1 = 1
    >>> # (the indifferent voter is not counted in the average at all).
    >>> MatrixWeightedMajority(['a > b', 'a ~ b'], indifference=None).as_df_
         a    b
    a  0.0  1.0
    b  0.0  0.0
    """

    def __init__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None,
                 default_converter: ConverterBallot=ConverterBallotToOrder(),
                 higher_vs_lower: Union[float, None] = 1., lower_vs_higher: Union[float, None] = 0.,
                 indifference: Union[float, None] = .5,
                 ordered_vs_unordered: Union[float, None] = 1., unordered_vs_ordered: Union[float, None] = 0.,
                 unordered_vs_unordered: Union[float, None] = .5,
                 ordered_vs_absent: Union[float, None] = None, absent_vs_ordered: Union[float, None] = None,
                 unordered_vs_absent: Union[float, None] = None, absent_vs_unordered: Union[float, None] = None,
                 absent_vs_absent: Union[float, None] = None,
                 default_score: float = 0.):
        self.higher_vs_lower = higher_vs_lower
        self.lower_vs_higher = lower_vs_higher
        self.indifference = indifference
        self.ordered_vs_unordered = ordered_vs_unordered
        self.unordered_vs_ordered = unordered_vs_ordered
        self.unordered_vs_unordered = unordered_vs_unordered
        self.ordered_vs_absent = ordered_vs_absent
        self.absent_vs_ordered = absent_vs_ordered
        self.unordered_vs_absent = unordered_vs_absent
        self.absent_vs_unordered = absent_vs_unordered
        self.absent_vs_absent = absent_vs_absent
        self.default_score = default_score
        super().__init__(ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
                         default_converter=default_converter)

    @cached_property
    def _gross_and_weights_(self):
        gross = {(c, d): 0. for c in self.candidates_ for d in self.candidates_}
        weights = {(c, d): 0. for c in self.candidates_ for d in self.candidates_}
        for ballot, weight, _ in self.profile_converted_.items():
            absent = self.candidates_ - ballot.candidates
            for i_class, indifference_class in enumerate(ballot.as_weak_order):
                indifference_class_as_list = list(indifference_class)
                for i, c in enumerate(indifference_class_as_list):
                    # Deal with other candidates of the indifference class
                    if self.indifference is not None:
                        for d in indifference_class_as_list[i + 1:]:
                            gross[(c, d)] += weight * self.indifference
                            gross[(d, c)] += weight * self.indifference
                            weights[(c, d)] += weight
                            weights[(d, c)] += weight
                    # Deal with ordered candidates with lower ranks
                    if self.higher_vs_lower is not None or self.lower_vs_higher is not None:
                        for lower_indifference_class in ballot.as_weak_order[i_class + 1:]:
                            for d in lower_indifference_class:
                                if self.higher_vs_lower is not None:
                                    gross[(c, d)] += weight * self.higher_vs_lower
                                    weights[(c, d)] += weight
                                if self.lower_vs_higher is not None:
                                    gross[(d, c)] += weight * self.lower_vs_higher
                                    weights[(d, c)] += weight
                    # Deal with unordered candidates
                    if self.ordered_vs_unordered is not None or self.unordered_vs_ordered is not None:
                        for d in ballot.candidates_not_in_b:
                            if self.ordered_vs_unordered is not None:
                                gross[(c, d)] += weight * self.ordered_vs_unordered
                                weights[(c, d)] += weight
                            if self.unordered_vs_ordered is not None:
                                gross[(d, c)] += weight * self.unordered_vs_ordered
                                weights[(d, c)] += weight
                    # Deal with absent candidates
                    if self.ordered_vs_absent is not None or self.absent_vs_ordered is not None:
                        for d in absent:
                            if self.ordered_vs_absent is not None:
                                gross[(c, d)] += weight + self.ordered_vs_absent
                                weights[(c, d)] += weight
                            if self.absent_vs_ordered is not None:
                                gross[(d, c)] += weight + self.absent_vs_ordered
                                weights[(d, c)] += weight
            if (self.unordered_vs_unordered is not None
                    or self.unordered_vs_absent is not None
                    or self.absent_vs_unordered is not None):
                unordered_as_list = list(ballot.candidates_not_in_b)
                for i, c in enumerate(unordered_as_list):
                    # Deal with other unordered candidates
                    if self.unordered_vs_unordered is not None:
                        for d in unordered_as_list[i + 1:]:
                            gross[(c, d)] += weight * self.unordered_vs_unordered
                            gross[(d, c)] += weight * self.unordered_vs_unordered
                            weights[(c, d)] += weight
                            weights[(d, c)] += weight
                    # Deal with absent candidates
                    for d in absent:
                        if self.unordered_vs_absent is not None:
                            gross[(c, d)] += weight * self.unordered_vs_absent
                            weights[(c, d)] += weight
                        if self.absent_vs_unordered is not None:
                            gross[(d, c)] += weight * self.absent_vs_unordered
                            weights[(d, c)] += weight
            if self.absent_vs_absent is not None:
                absent_as_list = list(absent)
                for i, c in enumerate(absent_as_list):
                    for d in absent_as_list[i + 1:]:
                        gross[(c, d)] += weight * self.absent_vs_absent
                        gross[(d, c)] += weight * self.absent_vs_absent
                        weights[(c, d)] += weight
                        weights[(d, c)] += weight
        return {'gross': gross, 'weights': weights}

    @cached_property
    def gross_(self):
        return self._gross_and_weights_['gross']

    @cached_property
    def weights_(self):
        return self._gross_and_weights_['weights']

    @cached_property
    def as_dict_(self):
        return {pair: self.gross_[pair] / w if w != 0 else self.default_score
                for pair, w in self.weights_.items()}
