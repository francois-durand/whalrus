from collections import Iterable
from functools import lru_cache


class LruCacheMixin(object):
    """A mixin that allows you to empty caches from lru_cached methods.

    Example:
    >>> from functools import lru_cache
    >>> class TestLru(LruCacheMixin):
    >>>     @lru_cache()
    >>>     def big_computation(self,n):
    >>>         print('doing the big computation...')
    >>>         return n*n
    >>> t = TestLru()
    >>> x = t.big_computation(3)
    doing the big computation...
    >>> x = t.big_computation(3)
    >>> t.empty_lru_caches()
    >>> x = t.big_computation(3)
    doing the big computation...
    """


    def empty_lru_caches(self):
        for field in dir(self):
            f = getattr(self, field)
            if callable(f) and hasattr(f, 'cache_info'):
                f.cache_clear()

