# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from flask import flash, make_response, redirect

from evobot.controllers.controller import app, request_post
from evobot.models.users import Users
from evobot.storage.mongo_cache import MongoCache


@app.route('/api/users/create', methods=['POST'])
@request_post
def create_account(login: str, password: str):
    try:
        _id = Users.create({'login': login, 'password': password})
    except:
        flash('Login not available.', 'error')
        return redirect('/users/create')
    return redirect('/users/login')


@app.route('/api/users', methods=['GET'])
def find_account():
    result = MongoCache.search("users")
    users = []
    for r in result:
        users.append(r)
    return str(users)


@app.route('/api/users/login', methods=['POST'])
@request_post
def connect(login: str, password: str):
    """
        :param str login: Login to connect
        :param str password: Password
    """
    token, expire_at = Users.log_in(login, password)
    if token:
        flash('You are successfully logged in.', 'success')
        res = make_response(redirect('/'))
        res.set_cookie('token', token, expires=expire_at)
        return res
    flash('Login and/or password mismatch', 'error')
    res = make_response(redirect('/users/login'))
    res.set_cookie('token', '', expires=0)
    return res


@app.route('/api/users/logout', methods=['GET'])
def disconnect():
    """
        Disconnect the current token (unvalidate it)
    """
    res = make_response(redirect('/'))

    res.set_cookie('token', '', expires=0)
    return res


def authorized(token: str):
    """
        Check if given token is authorized (=is connected / valid) or not

        :param str token: Token to check
        :return True / False depends on if token is valid or not
        :rtype: bool
    """
    return
