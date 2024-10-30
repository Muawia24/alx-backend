#!/usr/bin/python3
"""
FIFO caching
"""


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    def put(self, key, item):
        """
        Assign to the dictionary self.cache_data the item
        value for the key key.
        """
        cache_data = self.cache_data
        if key is None or item is None:
            return
        if key not in cache_data and len(cache_data) >= BaseCaching.MAX_ITEMS:
            chache_keys = sorted(cache_data.keys())
            first_item = chache_keys[0]
            print(f'DISCARD: {first_item}')
            del self.cache_data[first_item]

        self.cache_data[key] = item

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data.get(key)
