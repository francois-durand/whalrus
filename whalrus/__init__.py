# -*- coding: utf-8 -*-

"""Top-level package for Whalrus."""

__author__ = """Sylvain Bouveret, Yann Chevaleyre and François Durand"""
__email__ = 'fradurand@gmail.com'
__version__ = '0.4.6'

# Utils
from .utils.utils import cached_property, DeleteCacheMixin, parse_weak_order, set_to_list, set_to_str, dict_to_items, \
    dict_to_str, NiceSet, NiceDict, my_division, convert_number, take_closest

# Scales
from .scales.scale import Scale
from .scales.scale_from_list import ScaleFromList
from .scales.scale_from_set import ScaleFromSet
from .scales.scale_range import ScaleRange
from .scales.scale_interval import ScaleInterval

# Priority
from .priorities.priority import Priority
from .priorities.priority import PriorityUnambiguous
from .priorities.priority import PriorityAbstain
from .priorities.priority import PriorityAscending
from .priorities.priority import PriorityDescending
from .priorities.priority import PriorityRandom

# Ballots
from .ballots.ballot import Ballot
from .ballots.ballot_order import BallotOrder
from .ballots.ballot_levels import BallotLevels
from .ballots.ballot_one_name import BallotOneName
from .ballots.ballot_plurality import BallotPlurality
from .ballots.ballot_veto import BallotVeto

# Ballot Converters
from .converters_ballot.converter_ballot import ConverterBallot
from .converters_ballot.converter_ballot_general import ConverterBallotGeneral
from .converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from .converters_ballot.converter_ballot_to_strict_order import ConverterBallotToStrictOrder
from .converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from .converters_ballot.converter_ballot_to_veto import ConverterBallotToVeto
from .converters_ballot.converter_ballot_to_levels_interval import ConverterBallotToLevelsInterval
from .converters_ballot.converter_ballot_to_levels_range import ConverterBallotToLevelsRange
from .converters_ballot.converter_ballot_to_levels_list_numeric import ConverterBallotToLevelsListNumeric
from .converters_ballot.converter_ballot_to_levels_list_non_numeric import ConverterBallotToLevelsListNonNumeric
from .converters_ballot.converter_ballot_to_grades import ConverterBallotToGrades
from .converters_ballot.converter_ballot_to_levels import ConverterBallotToLevels

# Profile
from .profiles.profile import Profile

# Matrix
from .matrices.matrix import Matrix
from .matrices.matrix_weighted_majority import MatrixWeightedMajority
from .matrices.matrix_majority import MatrixMajority
from .matrices.matrix_ranked_pairs import MatrixRankedPairs
from .matrices.matrix_schulze import MatrixSchulze

# Elimination algorithms
from .eliminations.elimination import Elimination
from .eliminations.elimination_last import EliminationLast
from .eliminations.elimination_below_average import EliminationBelowAverage

# Scorers
from .scorers.scorer import Scorer
from .scorers.scorer_borda import ScorerBorda
from .scorers.scorer_bucklin import ScorerBucklin
from .scorers.scorer_levels import ScorerLevels
from .scorers.scorer_plurality import ScorerPlurality
from .scorers.scorer_positional import ScorerPositional
from .scorers.scorer_veto import ScorerVeto

# Voting Rules 1: General
from .rules.rule import Rule
from .rules.rule_score import RuleScore
from .rules.rule_score_num import RuleScoreNum
from .rules.rule_score_num_average import RuleScoreNumAverage
from .rules.rule_score_num_row_sum import RuleScoreNumRowSum
from .rules.rule_score_positional import RuleScorePositional
from .rules.rule_iterated_elimination import RuleIteratedElimination
from .rules.rule_sequential_elimination import RuleSequentialElimination
from .rules.rule_sequential_tie_break import RuleSequentialTieBreak

# Voting Rules 2: Particular
from .rules.rule_approval import RuleApproval
from .rules.rule_baldwin import RuleBaldwin
from .rules.rule_black import RuleBlack
from .rules.rule_borda import RuleBorda
from .rules.rule_bucklin_by_rounds import RuleBucklinByRounds
from .rules.rule_bucklin_instant import RuleBucklinInstant
from .rules.rule_condorcet import RuleCondorcet
from .rules.rule_coombs import RuleCoombs
from .rules.rule_copeland import RuleCopeland
from .rules.rule_irv import RuleIRV
from .rules.rule_k_approval import RuleKApproval
from .rules.rule_kim_roush import RuleKimRoush
from .rules.rule_majority_judgment import RuleMajorityJudgment
from .rules.rule_maximin import RuleMaximin
from .rules.rule_nanson import RuleNanson
from .rules.rule_plurality import RulePlurality
from .rules.rule_range_voting import RuleRangeVoting
from .rules.rule_ranked_pairs import RuleRankedPairs
from .rules.rule_schulze import RuleSchulze
from .rules.rule_simplified_dodgson import RuleSimplifiedDodgson
from .rules.rule_two_round import RuleTwoRound
from .rules.rule_veto import RuleVeto
