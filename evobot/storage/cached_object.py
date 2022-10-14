# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from .cache import Cache
from .mongo_cache import MongoCache


class CachedObject:
    _key = ''  # Used to identify the object, kind of table name.
    _store_db = False  # If True, then use MongoCache to persist it
    _no_pending = False  # If True, don't make use of pending queue, can be slower

    def __init__(self, key: str = ''):
        self._key = key or self._key

    def _default_vals(self) -> dict:
        default = dict()
        for attr in self._get_attributes():
            default.update({attr: getattr(self, attr)})
        return default

    def _get_attributes(self) -> list:
        """
            Return all available attribute of the object
        """
        attrs = dir(self)

        def is_attribute(a):
            is_attr = not callable(getattr(self, a))
            is_attr = is_attr and a[0] != '_'
            return is_attr
        return list(filter(is_attribute, attrs))

    def create(self, datas: dict):
        default_vals = self._default_vals()
        default_vals.update(datas)
        if self._store_db:
            _id = MongoCache.create(self._key, default_vals, self._no_pending)
        else:
            _id = Cache.create(self._key, default_vals)
        return _id

    def read(self, _id):
        if self._store_db:
            datas = MongoCache.read(self._key, _id)
        else:
            datas = Cache.read(self._key, _id)
        return datas

    def update(self, _id, datas: dict):
        if self._store_db:
            datas = MongoCache.update(self._key, _id, datas, self._no_pending)
        else:
            datas = Cache.update(self._key, _id, datas)

    def delete(self, _id):
        if self._store_db:
            datas = MongoCache.delete(self._key, _id, datas, self._no_pending)
        else:
            datas = Cache.delete(self._key, _id, datas)


existing_cached_object = dict()


def get_cached_object(key: str, cached_class=CachedObject):
    if key not in existing_cached_object:
        init_cached_object(key)

    cached_object = existing_cached_object[key]
    return cached_object


def init_cached_object(key: str, cached_class=CachedObject):
    existing_cached_object[key] = cached_class(key)
