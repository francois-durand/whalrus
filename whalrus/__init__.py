# -*- coding: utf-8 -*-

"""Top-level package for Whalrus."""

__author__ = """Sylvain Bouveret, Yann Chevaleyre and François Durand"""
__email__ = 'fradurand@gmail.com'
__version__ = '0.1.0'

from .utils.Utils import cached_property, DeleteCacheMixin, parse_weak_order, set_to_list, set_to_str, dict_to_items, \
    dict_to_str

from .SubPackage1.MyClass1 import MyClass1
from .SubPackage2.MyClass2 import MyClass2
from .SubPackage2.MyClass3 import MyClass3

from .ballots.Ballot import Ballot
from .ballots.UtilityBallot import UtilityBallot

#from .ballots.GradeBallot import GradeBallot
#from .ballots.RankingBallot import RankingBallot

from .voting_rules.VotingRule import VotingRule
from .voting_rules.Plurality import Plurality

from .profile import Profile
