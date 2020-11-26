=======
History
=======

---------------------------------------
0.4.4 (2020-11-26): Fix PyPI deployment
---------------------------------------

* Fix PyPI deployment.

----------------------------------
0.4.3 (2020-11-26): GitHub Actions
----------------------------------

* This patch concerns Whalrus' developpers only. To develop and maintain the package, it uses GitHub actions
  instead of additional services such as Travis-CI and ReadTheDocs.
* Use Codecov.
* Prepare support for Numpy documentation style (not used yet).
* Prepare support for notebooks in documentation (not used yet).

-------------------------------
0.4.2 (2019-08-22): Speeding Up
-------------------------------

* Minor patch to speed up the computation of the winner in some cases.

--------------------------------
0.4.1 (2019-04-01): Tie-breaking
--------------------------------

* Fix a bug related to random tie-break.
* In the arguments of class ``RuleRankedPairs``, the tie-break can be given directly, instead of having to go through
  the argument ``matrix``.

---------------------------
0.4.0 (2019-03-29): Schulze
---------------------------

* Implement Schulze rule.

--------------------------------
0.3.0 (2019-03-29): Ranked Pairs
--------------------------------

* Implement Ranked Pairs rule.

---------------------------------------------
0.2.1 (2019-03-28): Optimize argument passing
---------------------------------------------

* Optimize argument passing between child classes, their parent classes and their ``__call__`` function.

------------------------------------------
0.2.0 (2019-03-21): Classic voting systems
------------------------------------------

* First "real" release, where most classic voting systems are implemented.

---------------------------------
0.1.0 (2018-03-13): First release
---------------------------------

* First release on PyPI.
