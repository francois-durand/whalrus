from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.Scale import Scale
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from whalrus.converter_ballot.ConverterBallotToLevelsRange import ConverterBallotToLevelsRange
from whalrus.converter_ballot.ConverterBallotToLevelsListNumeric import ConverterBallotToLevelsListNumeric


class ConverterBallotToGrades(ConverterBallot):
    """
    Default converter to a ballot using grades.

    :param scale: a :class:`Scale`. If specified, then the ballot will be converted to this (numeric) scale. If it is
        None, then any ballot that is of class :class:`BallotLevels` and numeric will be kept as it is, and any other
        ballot will converted to the :class:`ScaleInterval` with bounds 0. and 1.
    :param borda_unordered_give_points: when converting a :class:`BallotOrder`, we use Borda scores as a calculation
        step. This parameter decides whether unordered candidates of the ballot give points to ordered candidates.
        Cf. meth:`BallotOrder.borda`.

    This is a default converter to a ballot using grades. It tries to infer the type of input and converts it to
    a :class:`BallotLevels`, with a numeric scale. It is a wrapper for the specialized converters
    :class:`ConverterBallotToLevelsInterval`, :class:`ConverterBallotToLevelsRange`,
    and :class:`ConverterBallotToLevelsListNumeric`.

    Typical usages:

    >>> ballot = BallotLevels({'a': 100, 'b': 57}, scale=ScaleRange(0, 100))
    >>> ConverterBallotToGrades(scale=ScaleInterval(low=0., high=10.))(ballot)
    BallotLevels({'a': 10.0, 'b': 5.7}, candidates={'a', 'b'}, scale=ScaleInterval(low=0.0, high=10.0))
    >>> ConverterBallotToGrades(scale=ScaleRange(low=0, high=10))(ballot)
    BallotLevels({'a': 10, 'b': 6}, candidates={'a', 'b'}, scale=ScaleRange(low=0, high=10))
    >>> ConverterBallotToGrades(scale=ScaleFromSet({0, 2, 4, 10}))(ballot)
    BallotLevels({'a': 10, 'b': 4}, candidates={'a', 'b'}, scale=ScaleFromSet(levels={0, 2, 4, 10}))

    >>> ballot = BallotLevels({'a': 'Good', 'b': 'Medium'}, scale=ScaleFromList(['Bad', 'Medium', 'Good']))
    >>> ConverterBallotToGrades()(ballot)
    BallotLevels({'a': 1.0, 'b': 0.5}, candidates={'a', 'b'}, scale=ScaleInterval(low=0.0, high=1.0))

    For more examples, cf. :class:`ConverterBallotToLevelsInterval`, :class:`ConverterBallotToLevelsRange`,
    and :class:`ConverterBallotToLevelsListNumeric`.
    """

    def __init__(self, scale: Scale = None, borda_unordered_give_points: bool = True):
        self.scale = scale
        self.borda_unordered_give_points = borda_unordered_give_points
        if scale is None:
            self._aux_converter = ConverterBallotToLevelsInterval(
                scale=ScaleInterval(low=0., high=1.), borda_unordered_give_points=borda_unordered_give_points)
        elif isinstance(scale, ScaleInterval):
            self._aux_converter = ConverterBallotToLevelsInterval(
                scale=scale, borda_unordered_give_points=borda_unordered_give_points)
        elif isinstance(scale, ScaleRange):
            self._aux_converter = ConverterBallotToLevelsRange(
                scale=scale, borda_unordered_give_points=borda_unordered_give_points)
        elif isinstance(scale, ScaleFromList):
            self._aux_converter = ConverterBallotToLevelsListNumeric(
                scale=scale, borda_unordered_give_points=borda_unordered_give_points)
        else:
            raise NotImplementedError

    def __call__(self, x: object, candidates: set =None) -> BallotLevels:
        if self.scale is None and isinstance(x, BallotLevels) and x.is_numeric:
            return x.restrict(candidates=candidates)
        return self._aux_converter(x, candidates=candidates)
