# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from flask import Flask, request
from flask import render_template as flask_render_template

from functools import wraps
from os import urandom
import inspect

from evobot.models import Users


app = Flask(__name__, template_folder='ui/templates')
app.secret_key = urandom(32)


def get_default_context():
    token = request.cookies.get('token', '')

    context = {
        'user': Users.who_is_logged_in(token),
    }
    return context


def render_template(template, **context):
    # Kind of override of render_template from flask, but with custom context by default.
    default_context = get_default_context()
    default_context.update(context)
    return flask_render_template(template, **default_context)


def request_post(function):
    @wraps(function)
    def _request_param():
        args = inspect.signature(function).parameters
        values = []
        for arg in args:
            values.append(request.form.get(arg))
        return function(*values)
    return _request_param
