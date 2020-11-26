# -*- coding: utf-8 -*-

"""Top-level package for Whalrus."""

__author__ = """Sylvain Bouveret, Yann Chevaleyre and François Durand"""
__email__ = 'fradurand@gmail.com'
__version__ = '0.4.4'

# Utils
from .utils.Utils import cached_property, DeleteCacheMixin, parse_weak_order, set_to_list, set_to_str, dict_to_items, \
    dict_to_str, NiceSet, NiceDict, my_division, convert_number, take_closest

# Scales
from .scale.Scale import Scale
from .scale.ScaleFromList import ScaleFromList
from .scale.ScaleFromSet import ScaleFromSet
from .scale.ScaleRange import ScaleRange
from .scale.ScaleInterval import ScaleInterval

# Priority
from .priority.Priority import Priority
from .priority.Priority import PriorityUnambiguous
from .priority.Priority import PriorityAbstain
from .priority.Priority import PriorityAscending
from .priority.Priority import PriorityDescending
from .priority.Priority import PriorityRandom

# Ballots
from .ballot.Ballot import Ballot
from .ballot.BallotOrder import BallotOrder
from .ballot.BallotLevels import BallotLevels
from .ballot.BallotOneName import BallotOneName
from .ballot.BallotPlurality import BallotPlurality
from .ballot.BallotVeto import BallotVeto

# Ballot Converters
from .converter_ballot.ConverterBallot import ConverterBallot
from .converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from .converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from .converter_ballot.ConverterBallotToStrictOrder import ConverterBallotToStrictOrder
from .converter_ballot.ConverterBallotToPlurality import ConverterBallotToPlurality
from .converter_ballot.ConverterBallotToVeto import ConverterBallotToVeto
from .converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from .converter_ballot.ConverterBallotToLevelsRange import ConverterBallotToLevelsRange
from .converter_ballot.ConverterBallotToLevelsListNumeric import ConverterBallotToLevelsListNumeric
from .converter_ballot.ConverterBallotToLevelsListNonNumeric import ConverterBallotToLevelsListNonNumeric
from .converter_ballot.ConverterBallotToGrades import ConverterBallotToGrades
from .converter_ballot.ConverterBallotToLevels import ConverterBallotToLevels

# Profile
from .profile.Profile import Profile

# Matrix
from .matrix.Matrix import Matrix
from .matrix.MatrixWeightedMajority import MatrixWeightedMajority
from .matrix.MatrixMajority import MatrixMajority
from .matrix.MatrixRankedPairs import MatrixRankedPairs
from .matrix.MatrixSchulze import MatrixSchulze

# Elimination algorithms
from .elimination.Elimination import Elimination
from .elimination.EliminationLast import EliminationLast
from .elimination.EliminationBelowAverage import EliminationBelowAverage

# Scorers
from .scorer.Scorer import Scorer
from .scorer.ScorerBorda import ScorerBorda
from .scorer.ScorerBucklin import ScorerBucklin
from .scorer.ScorerLevels import ScorerLevels
from .scorer.ScorerPlurality import ScorerPlurality
from .scorer.ScorerPositional import ScorerPositional
from .scorer.ScorerVeto import ScorerVeto

# Voting Rules 1: General
from .rule.Rule import Rule
from .rule.RuleScore import RuleScore
from .rule.RuleScoreNum import RuleScoreNum
from .rule.RuleScoreNumAverage import RuleScoreNumAverage
from .rule.RuleScoreNumRowSum import RuleScoreNumRowSum
from .rule.RuleScorePositional import RuleScorePositional
from .rule.RuleIteratedElimination import RuleIteratedElimination
from .rule.RuleSequentialElimination import RuleSequentialElimination
from .rule.RuleSequentialTieBreak import RuleSequentialTieBreak

# Voting Rules 2: Particular
from .rule.RuleApproval import RuleApproval
from .rule.RuleBaldwin import RuleBaldwin
from .rule.RuleBlack import RuleBlack
from .rule.RuleBorda import RuleBorda
from .rule.RuleBucklinByRounds import RuleBucklinByRounds
from .rule.RuleBucklinInstant import RuleBucklinInstant
from .rule.RuleCondorcet import RuleCondorcet
from .rule.RuleCoombs import RuleCoombs
from .rule.RuleCopeland import RuleCopeland
from .rule.RuleIRV import RuleIRV
from .rule.RuleKApproval import RuleKApproval
from .rule.RuleKimRoush import RuleKimRoush
from .rule.RuleMajorityJudgment import RuleMajorityJudgment
from .rule.RuleMaximin import RuleMaximin
from .rule.RuleNanson import RuleNanson
from .rule.RulePlurality import RulePlurality
from .rule.RuleRangeVoting import RuleRangeVoting
from .rule.RuleRankedPairs import RuleRankedPairs
from .rule.RuleSchulze import RuleSchulze
from .rule.RuleSimplifiedDodgson import RuleSimplifiedDodgson
from .rule.RuleTwoRound import RuleTwoRound
from .rule.RuleVeto import RuleVeto

# Examples of documentation
from .SubPackage1.MyClass1 import MyClass1
from .SubPackage2.MyClass2 import MyClass2
from .SubPackage2.MyClass3 import MyClass3
