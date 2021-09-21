from personalsite import app
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect
import os
import secret

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0