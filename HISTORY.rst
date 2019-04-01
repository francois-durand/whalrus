=======
History
=======

0.4.1 (2019-04-01)
------------------

* Fix a bug related to random tie-break.
* In the arguments of :class:`RuleRankedPairs`, the tie-break can be given directly, instead of having to go through
  the argument ``matrix``.

0.4.0 (2019-03-29)
------------------

* Implement Schulze rule.

0.3.0 (2019-03-29)
------------------

* Implement Ranked Pairs rule.

0.2.1 (2019-03-28)
------------------

* Optimize argument passing between child classes, their parent classes and their ``__call__`` function.

0.2.0 (2019-03-21)
------------------

* First "real" release, where most classic voting systems are implemented.

0.1.0 (2018-03-13)
------------------

* First release on PyPI.
