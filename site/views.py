from certhasher import app
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect
import numpy as np
import os

@app.route('/')
def home():
    render_template('home.html')

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0