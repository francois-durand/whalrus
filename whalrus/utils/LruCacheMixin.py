from collections import Iterable
from functools import lru_cache


class LruCacheMixin(object):
    def empty_lru_caches(self):
        """
        """
        for field in dir(self):
            f = getattr(self, field)
            if callable(f) and hasattr(f, 'cache_info'):
                f.cache_clear()

