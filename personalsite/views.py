from personalsite import app, jwt
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect, jsonify, Response
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, set_access_cookies, unset_jwt_cookies
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
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if username != secret.USERNAME or password != secret.PASSWORD:
            return 'incorrect username'

        # additional_claims = {'jwt':'some audience', 'hello':'there'}
        # access_token = create_access_token(identity=username, additional_claims=additional_claims)

        # res = make_response()
        # res.headers["Access-Control-Allow-Origin"] = "*"
        # # res.headers['jwt'] = access_token

        # set_access_cookies(res, access_token)
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        access_token = create_access_token(identity="example_user")
        set_access_cookies(response, access_token)

        return response
        
@app.route('/dastoryhub', methods=['GET'])
@jwt_required()   # https://flask-jwt-extended.readthedocs.io/en/stable/_modules/flask_jwt_extended/view_decorators/#jwt_required
                # The wrap() provided by python is good for defining wrapper functions. helps preserve the meta data (__name__) of the original function.
def blog():
    data_claim = get_jwt()
    return jsonify(hello=data_claim['hello'])
    return render_template('bloglist.html')

@app.route('/dastory', methods=['GET'])
@jwt_required()
def blogindv():
    story_num = request.args.get('story', default=1, type=int)
    return render_template('blogindividual.html')

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
    # for removing tokens
    res = make_response(redirect(url_for('signin')))
    unset_jwt_cookies(res)
    return res