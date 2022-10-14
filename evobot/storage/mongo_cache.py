# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from pymongo import MongoClient
import schedule
from threading import Thread

from .cache import Cache

mongo_client = MongoClient('mongo', 27017)
mongo_db = mongo_client['evobot']


class MongoCache(Cache.__class__):
    """
        Used to store and save data in mongo db
        Override Cache and store every change in a pending queue.
        Then everything is stored through time.

        create(key: str, datas: dict) -> int
        update(key: str, oid: int, datas: dict)
        delete(key: str, oid: int)
    """

    def __init__(self):
        super().__init__()
        self._pending_operation = {
            'created': dict(),
            'updated': dict(),
            'deleted': dict(),
        }
        self._tmp_id_to_mongo = dict()
        self.threads = 0

    @property
    def _pending_created(self):
        return self._pending_operation['created']

    @property
    def _pending_updated(self):
        return self._pending_operation['updated']

    @property
    def _pending_deleted(self):
        return self._pending_operation['deleted']

    def create(self, key: str, datas: dict, no_pending: bool = False) -> int:
        created_id = super().create(key, datas)
        if key not in self._pending_created:
            self._pending_created[key] = []
        self._pending_created[key].append(datas)
        if no_pending:
            created_id = self._run_pending_created(key, return_ids=True)
        return created_id

    def update(self, key: str, _id: int, datas: dict):
        super().update(key, _id, datas)
        if key not in self._pending_updated:
            self._pending_updated[key] = dict()
        if _id not in self._pending_updated[key]:
            self._pending_created[key][_id] = dict()
        self._pending_created[key][_id].update(datas)

    def delete(self, key: str, _id: int):
        super().delete(key, _id)
        if key not in self._pending_deleted:
            self._pending_deleted[key] = []
        self._pending_created[key].append(_id)

    def read(self, key: str, _id: int, *args, **kwargs):
        """
            Read datas of specified oid of keys

            :param str key: Key to store datas (kind of "table" name)
            :param int _id: associated id
            :return value of key/id
        """
        def read_from_mongo():
            return mongo_db[key].find_one({'_id': _id}, *args, **kwargs)
        _id_datas = self._datas.get(key, dict()).get(_id, read_from_mongo())  # If crashed here -> _id doesn't exists
        return _id_datas

    def search(self, key: str, domain: dict = dict(), *args, **kwargs):
        return mongo_db[key].find(domain, *args, **kwargs)

    def _run_pending(self):
        Thread(target=self._run_pending_created).start()
        # Thread(target=self._run_pending_updated).start()
        # Thread(target=self._run_pending_deleted).start()

    def _run_pending_created(self, key_filter: str = '', return_ids: bool = False):
        self.threads += 1
        created_ids = list()
        if key_filter:
            run_on = {key_filter: self._pending_created.get(key_filter)}
        else:
            run_on = self._pending_created
        for key, datas in run_on.items():
            for i in range(len(datas)):
                data = datas.pop()
                print("Popped:", data)
                created_ids.append(mongo_db[key].insert_one(data))
        self.threads -= 1
        if return_ids:
            return created_ids[0] if len(created_ids) == 1 else created_ids

    def create_unique_index(self, key, keys):
        mongo_db[key].create_index(keys, unique=True)


MongoCache = MongoCache()

schedule.every(2).minutes.do(MongoCache._run_pending_created)
