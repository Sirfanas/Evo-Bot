# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'


class Cache:
    """
        Used to quickly store data.

        create(key: str, datas: dict) -> int
        read(key: str, oid: int) -> dict
        update(key: str, oid: int, datas: dict)
        delete(key: str, oid: int)
    """

    def __init__(self):
        self._datas = dict()
        self._sequences = dict()

    def _ensure_key(self, key: str):
        if key not in self._datas:
            self._datas[key] = dict()

    def create(self, key: str, datas: dict) -> int:
        """
            Store datas in specified keys

            :param str key: Key to store datas (kind of "table" name)
            :param dict datas: Datas to store as dict
            :return created id
            :rtype: int
        """
        self._ensure_key(key)
        new_id = self._get_tmp_id(key)
        self._datas[key][new_id] = datas
        return new_id

    def read(self, key: str, _id: int) -> dict:
        """
            Read datas of specified oid of keys

            :param str key: Key to store datas (kind of "table" name)
            :param int _id: associated id
            :return value of key/id
        """
        self._ensure_key(key)
        _id_datas = self._datas[key][_id]  # If crashed here -> oid doesn't exists
        return _id_datas

    def update(self, key: str, _id: int, datas: dict):
        """
            Update data of key/oid with value

            :param str key: Key to store datas (kind of "table" name)
            :param int oid: associated id
            :param dict datas: Value to update
        """
        self._ensure_key(key)
        self._datas[key][_id].update(datas)

    def delete(self, key: str, _id: int):
        """
            Delete record of key/id, can't be restored !!

            :param str key: Key to store datas (kind of "table" name)
            :param int oid: associated id
        """
        self._ensure_key(key)
        del self._datas[key][_id]  # If crashed here -> _id doesn't exist

    def _get_tmp_id(self, key: str) -> str:
        """
            Return a temporary id based on _sequences
            if not set then initialize at 1
            automaticly increment it.

            :param str key: Key to store datas (kind of "table" name)
            :return generated id
            :rtype: int
        """
        current_id = self._sequences.get(key, 0)
        next_id = current_id + 1
        self._sequences[key] = next_id
        return 'tmp_%s' % (next_id)


Cache = Cache()
