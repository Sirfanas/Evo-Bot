# coding: utf-8

from .cache import Cache


class CachedObject:
    _key = ''  # Used to identify the object, kind of table name.

    def __init__(self, key: str=''):
        self._key = key or self._key
        self._oid = 0
        self._datas = dict()

    def _debug(self):
        return {
            '_key': self._key,
            '_oid': self._oid,
            '_datas': self._datas,
        }

    def _default_vals(self):
        return dict()

    def set_current_oid(self, oid: int):
        self._oid = oid
        self.read()

    def create(self, datas: dict):
        default_vals = self._default_vals()
        default_vals.update(datas)
        oid = Cache.create(self._key, default_vals)
        self.set_current_oid(oid)
        return self

    def read(self):
        self._datas = Cache.read(self._key, self._oid)
        return self._datas

    def update(self, datas: dict):
        Cache.update(self._key, self._oid, datas)

    def delete(self):
        Cache.delete(self._key, self._oid)


existing_cached_object = dict()

def get_cached_object(key: str, oid: int=0, cached_class=CachedObject):
    if key not in existing_cached_object:
        existing_cached_object[key] = cached_class(key)

    cached_object = existing_cached_object[key]
    if oid:
        cached_object.set_current_oid(oid)
    return cached_object
