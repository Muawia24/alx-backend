#!/usr/bin/python3
"""
  MRU Caching
"""


from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """
    Class MRUCache
    Discard the most recently used item (MRU algorithm)
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

        if key not in self.cache_data:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                k, _ = self.cache_data.popitem(True)
                print(f'DISCARD: {k}')

            self.cache_data[key] = item
            self.cache_data.move_to_end(key, last=True)
        else:
            self.cache_data[key] = item

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.move_to_end(key, last=True)

        return self.cache_data.get(key)
