# -*- coding: utf-8 -*-

"""Top-level package for Whalrus."""

__author__ = """Sylvain Bouveret, Yann Chevaleyre and François Durand"""
__email__ = 'fradurand@gmail.com'
__version__ = '0.1.0'

# Utils
from .utils.Utils import cached_property, DeleteCacheMixin, parse_weak_order, set_to_list, set_to_str, dict_to_items, \
    dict_to_str, NiceSet, NiceDict

# Scales
from .scale.Scale import Scale
from .scale.ScaleFromList import ScaleFromList
from .scale.ScaleFromSet import ScaleFromSet
from .scale.ScaleRange import ScaleRange
from .scale.ScaleInterval import ScaleInterval

# Priority
from .priority.Priority import Priority

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
from .converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from .converter_ballot.ConverterBallotToLevelsRange import ConverterBallotToLevelsRange
from .converter_ballot.ConverterBallotToLevelsListNonNumeric import ConverterBallotToLevelsListNonNumeric
from .converter_ballot.ConverterBallotToLevelsListNumeric import ConverterBallotToLevelsListNumeric
from .converter_ballot.ConverterBallotToVeto import ConverterBallotToVeto

# Profile
from .profile.Profile import Profile

# Matrix
from .matrix.Matrix import Matrix
from .matrix.MatrixWeightedMajority import MatrixWeightedMajority
from .matrix.MatrixMajority import MatrixMajority

# Elimination algorithms
from .elimination.Elimination import Elimination
from .elimination.EliminationLast import EliminationLast
from .elimination.EliminationBelowAverage import EliminationBelowAverage

# Voting Rules: basic abstract classes
from .rule.Rule import Rule
from .rule.RuleScore import RuleScore

# Voting Rules: basic rules
from .rule.RuleCondorcet import RuleCondorcet
from .rule.RulePlurality import RulePlurality
from .rule.RuleBorda import RuleBorda
from .rule.RuleMaximin import RuleMaximin
from .rule.RuleScorePositional import RuleScorePositional
from .rule.RuleKApproval import RuleKApproval
from .rule.RuleVeto import RuleVeto
from .rule.RuleCopeland import RuleCopeland

# Voting Rules: "meta-rules"
from .rule.RuleIteratedElimination import RuleIteratedElimination
from .rule.RuleSequentialElimination import RuleSequentialElimination
from .rule.RuleSequentialTieBreak import RuleSequentialTieBreak

# Voting Rules: complex rules (using meta-rules)
from .rule.RuleBlack import RuleBlack
from .rule.RuleBaldwin import RuleBaldwin
from .rule.RuleNanson import RuleNanson
from .rule.RuleIRV import RuleIRV
from .rule.RuleCoombs import RuleCoombs
from .rule.RuleKimRoush import RuleKimRoush

# Examples of documentation
from .SubPackage1.MyClass1 import MyClass1
from .SubPackage2.MyClass2 import MyClass2
from .SubPackage2.MyClass3 import MyClass3

# Tutorials
from .tutorial.tutorial import quick_start, computed_attributes, general_syntax, under_the_hood, combine_rules, \
    change_candidates
