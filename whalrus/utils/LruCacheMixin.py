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
from collections import Iterable
from functools import lru_cache


class LruCacheMixin(object):
    """A mixin that allows you to empty caches from lru_cached methods.

    TODO: remove when obsolete

    Example:

    >>> from functools import lru_cache
    >>>
    >>> class TestLru(LruCacheMixin):
    ...     @lru_cache()
    ...     def big_computation(self,n):
    ...         print('I have to do the big computation...')
    ...         return n*n
    >>>
    >>> t = TestLru()
    >>> t.big_computation(3)
    I have to do the big computation...
    9
    >>> t.big_computation(3)
    9
    >>> t.empty_lru_caches()
    >>> t.big_computation(3)
    I have to do the big computation...
    9
    """


    def empty_lru_caches(self):
        for field in dir(self):
            f = getattr(self, field)
            if callable(f) and hasattr(f, 'cache_info'):
                f.cache_clear()

