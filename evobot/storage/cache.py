# coding: utf-8

class Cache:
    """
        Used to quickly store data, will be bridged with a real database.
    """

    def __init__(self):
        self._datas = dict()
        self._sequences = dict()

    def create(self, key, datas: dict) -> int:
        """
            Store datas in specified keys

            :param key: Any serializable value (str, int...)
            :param dict datas: Datas to store as dict
            :return created id
            :rtype: int
        """
        if key not in self._datas:
            self._datas[key] = dict()
        new_id = self._next_id(key)
        self._datas[key][new_id] = datas
        return new_id

    def read(self, key, oid: int):
        """
            Read datas of specified oid of keys

            :param key: Any serializable value (str, int...)
            :param int oid: associated id
            :return value of key/id
        """
        key_data = self._datas[key]  # If crashed here -> key doesn't exists
        oid_datas = key_data[oid]  # If crashed here -> oid doesn't exists
        return oid_datas

    def update(self, key, oid: int, value: dict):
        """
            Update data of key/oid with value

            :param key: Any serializable value (str, int...)
            :param int oid: associated id
            :param dict value: Value to update
        """
        self._datas[key][oid].update(value)

    def delete(self, key, oid: int):
        """
            Delete record of key/id, can't be restored !!

            :param key: Any serializable value (str, int...)
            :param int oid: associated id
        """
        del self._datas[key][oid]

    def _next_id(self, key) -> int:
        """
            Return the next id based on _sequences
            if not set then initialize at 1
            automaticly increment it.

            :param key: Any serializable value (str, int...)
            :return generated id
            :rtype: int
        """
        current_id = self._sequences.get(key, 0)
        next_id = current_id + 1
        self._sequences[key] = next_id
        return next_id
