# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from evobot.controllers.controller import app, render_template


@app.route('/users/create')
def auth_create():
    return render_template('users_create.html')


@app.route('/users/login')
def auth_login():
    return render_template('users_login.html')
