import os
import time
import pickle
import hashlib


class DiskCache:
    def __init__(self, cache_dir="cache", default_ttl=3600):
        """
        cache data initial
        :param cache_dir:
        :param default_ttl:
        """
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        os.makedirs(cache_dir, exist_ok=True)

    def _key_to_path(self, key):
        """
        get the data by key
        :param key:
        :return:
        """
        key_hash = hashlib.md5(str(key).encode()).hexdigest()
        return os.path.join(self.cache_dir, key_hash + ".cache")

    def get_hash_value(self, key):
        """
        get key hash value
        :param key:
        :return:
        """
        return hashlib.md5(str(key).encode()).hexdigest()

    def set(self, key, value, ttl=None):
        """
        save the data
        :param key:
        :param value:
        :param ttl:
        """
        expire_at = time.time() + (ttl or self.default_ttl)
        path = self._key_to_path(key)
        with open(path, "wb") as f:
            pickle.dump((value, expire_at), f)

    def get(self, key, default=None):
        """
        get the data by key
        :param key:
        :param default:
        :return:
        """
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
        """
        delete the data
        :param key:
        """
        path = self._key_to_path(key)
        if os.path.exists(path):
            os.remove(path)

    def clear(self):
        """
        clear all data
        """
        for file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, file))


CACHE = DiskCache()


