from personalsite import app, jwt
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
import os
import secret

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    if request.method == 'POST':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username != secret.USERNAME or password != secret.PASSWORD:
            return 'incorrect username'

        additional_claims = {'aud':'some audience', 'hello':'there'}
        access_token = create_access_token(username, additional_claims=additional_claims)
        return jsonify(access_token=access_token)
        
@app.route('/dablog', methods=['GET'])
@jwt_required   # https://flask-jwt-extended.readthedocs.io/en/stable/_modules/flask_jwt_extended/view_decorators/#jwt_required
                # The wrap() provided by python is good for defining wrapper functions. helps preserve the meta data (__name__) of the original function.
def blog():
    data_claim = get_jwt()
    return jsonify(hello=data_claim['hello'])
    return render_template('bloglist.html')

@app.route('/dablog', methods=['GET'])
@jwt_required
def blogindv():
    story_num = request.args.get('story', default=1, type=int)
    return render_template('blogidnv.html')