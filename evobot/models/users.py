# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from flask import session, request

import datetime
from os import urandom
from hashlib import pbkdf2_hmac, sha512

from evobot.storage import CachedObject
from evobot.storage.mongo_cache import MongoCache


def hash_password(password: str, salt: bytes = None) -> dict:
    """
        Hash and return hashed password and salt as dict.

        :param str password: Password to hash
        :param str salt: Salt to hash password
        :return {
            'key': 'hashed password',
            'salt': b'Salt',
        }
    """
    salt = salt or urandom(32)
    key = pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return {'key': key, 'salt': salt}


def _date_token():
    return datetime.datetime.now()


def _generate_token(login: str):
    today = _date_token()
    token = '%s%s' % (login, today.strftime('%Y-%m-%d'))
    token = token.encode()
    return sha512(token).hexdigest(), today


class Users(CachedObject):
    _key = 'users'
    _store_db = True
    _no_pending = True

    login = 'login'
    password = 'password'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        MongoCache.create_unique_index(self._key, [('login', 1)])

    def create(self, datas: dict):
        assert datas.get('password'), 'Password must be provided !'
        assert datas.get('login'), 'Login must be provided !'

        hash_datas = hash_password(datas['password'])
        datas['password'] = hash_datas['key']
        datas['salt'] = hash_datas['salt']
        return super().create(datas)

    def log_in(self, login: str, passwd: str):
        user = MongoCache.search(self._key, {'login': login}, limit=1)[0]
        password_matches = user.get('password') == hash_password(passwd, user.get('salt'))['key']
        if password_matches:
            token, date = _generate_token(login)
            expires_at = date + datetime.timedelta(days=1)
            MongoCache.create('users.token', {
                'users_id': user.get('_id'),
                'token': token,
                'date': date,
                'expires_at': expires_at
            }, no_pending=True)
            return token, expires_at
        else:
            return False, False

    def is_logged_in(self, token: str):
        token = MongoCache.search('users.token', {
            'token': token,
            'expires_at': {'$gte': datetime.datetime.now()}}, limit=1)
        return bool(token)

    def who_is_logged_in(self, token: str):
        token = MongoCache.search('users.token', {
            'token': token,
            'expires_at': {'$gte': datetime.datetime.now()}}, limit=1)
        for tok in token:
            return MongoCache.read('users', tok.get('users_id'), projection=['login'])
        return dict()


Users = Users()
