import os
import time
import pickle
import hashlib


class DiskCache:
    def __init__(self, cache_dir="cache", default_ttl=3600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        os.makedirs(cache_dir, exist_ok=True)

    def _key_to_path(self, key):
        key_hash = hashlib.md5(str(key).encode()).hexdigest()
        return os.path.join(self.cache_dir, key_hash + ".cache")

    def get_hash_value(self, key):
        return hashlib.md5(str(key).encode()).hexdigest()

    def set(self, key, value, ttl=None):
        expire_at = time.time() + (ttl or self.default_ttl)
        path = self._key_to_path(key)
        with open(path, "wb") as f:
            pickle.dump((value, expire_at), f)

    def get(self, key, default=None):
        path = self._key_to_path(key)
        if not os.path.exists(path):
            return default

        try:
            with open(path, "rb") as f:
                value, expire_at = pickle.load(f)
        except Exception:
            return default

        # if time.time() > expire_at:
        #     os.remove(path)
        #     return default

        return value

    def delete(self, key):
        path = self._key_to_path(key)
        if os.path.exists(path):
            os.remove(path)

    def clear(self):
        for file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, file))


CACHE = DiskCache()


