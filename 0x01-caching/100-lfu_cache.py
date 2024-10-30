#!/usr/bin/python3
"""
  LRU Caching
"""


from collections import OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFU Caching Class
    Discard the least frequency used item
    """
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()
        self.freq_counts = {}
        self.usage_order = OrderedDict()

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
                self.evict()

            self.freq_counts[key] = 1
            self.cache_data[key] = item
            self.usage_order[key] = None

        else:
            self.freq_counts[key] += 1
            self.cache_data[key] = item
            self.usage_order.move_to_end(key)

    def get(self, key):
        """
        Return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data:
            return None
        self.freq_counts[key] += 1
        self.usage_order.move_to_end(key)
        return self.cache_data.get(key)

    def evict(self):
        """ Find the least frequently used items """
        min_freq = min(self.freq_counts.values())
        lfu_keys = [k for k, v in self.freq_counts.items() if v == min_freq]

        # From the least frequently used, evict the least recently used
        lru_key = min(lfu_keys, key=lambda k: list(
            self.usage_order.keys()).index(k))

        # Discard the item
        print(f'DISCARD: {lru_key}')
        del self.cache_data[lru_key]
        del self.freq_counts[lru_key]
        del self.usage_order[lru_key]
