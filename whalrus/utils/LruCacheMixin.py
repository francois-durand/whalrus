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

