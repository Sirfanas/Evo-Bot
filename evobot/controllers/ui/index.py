# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from evobot.controllers.controller import app, render_template


@app.route('/')
def root():
    return render_template('index.html')
