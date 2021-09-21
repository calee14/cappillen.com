from personalsite import app
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect
import os
import secret

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signin')
def signin():
    return render_template('signin')

@app.route('/dablog')
def blog():
    return render_template('bloglist')

@app.route('/dablog')
def blogindv():
    return render_template('blogidnv')

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0