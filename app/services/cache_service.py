from cachetools import TTLCache

class CacheService:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=300)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value