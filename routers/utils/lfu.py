from collections import defaultdict


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.frequency = defaultdict(int)
        self.min_frequency = 10

    def get(self, key):
        if key in self.cache:
            value, freq = self.cache[key]
            if freq == self.min_frequency and not any(self.frequency[key] > self.frequency[k] for k in self.cache):
                self.min_frequency += 1
            return value
        else:
            return None

    def put(self, key, value):
        if self.capacity <= 0:
            return

        if key in self.cache:
            self.cache[key] = (value, self.frequency[key] + 1)
            self.frequency[key] += 1
        else:
            if len(self.cache) >= self.capacity:
                # Find and remove the least frequently used item(s)
                to_remove = [k for k, v in self.frequency.items() if v == self.min_frequency]
                for k in to_remove:
                    del self.cache[k]
                    del self.frequency[k]
                self.min_frequency += 1

            self.cache[key] = (value, 1)
            self.frequency[key] = 1
