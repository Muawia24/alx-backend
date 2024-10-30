#!/usr/bin/python3
"""
 LIFO Caching
"""


from collections import OrderedDict
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
     LIFO Caching class
     Discards the last item put in cache (LIFO algorithm)
     """
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data the item
        value for the key key.
        """
        cache_data = self.cache_data
        if key is None or item is None:
            return

        if key not in cache_data and len(cache_data) >= BaseCaching.MAX_ITEMS:
            chache_key = list(self.cache_data.keys())[-1]
            
            last_item = self.cache_data.pop(chache_key)
            print(f'DISCARD: {chache_key}')

        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data.get(key)
