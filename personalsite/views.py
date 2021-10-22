from personalsite import app, jwt
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect, jsonify, Response
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, set_access_cookies, unset_jwt_cookies
import os
from os import listdir
from os.path import isfile, join
import secret
from datetime import datetime

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

        additional_claims = {'jwt':'some audience', 'hello':'there'}

        # create res to set cookie and redirect to blog
        response = make_response(redirect(url_for('blog')), 302) # 302 is the status code for redirect https://stackoverflow.com/questions/47464961/flask-routing-problems
        response.headers['Access-Control-Allow-Origin'] = '*'
        access_token = create_access_token(identity=username, additional_claims=additional_claims)
        set_access_cookies(response, access_token)

        return response

stories = [{"title": 'hello there', "paragraphs": ['hello', 'there']}]    
@app.route('/dastoryhub', methods=['GET'])
@jwt_required()     # https://flask-jwt-extended.readthedocs.io/en/stable/_modules/flask_jwt_extended/view_decorators/#jwt_required
                    # The wrap() provided by python is good for defining wrapper functions. helps preserve the meta data (__name__) of the original function.
def blog():
    data_claim = get_jwt()
    claims = jsonify(hello=data_claim['hello'])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    blog_path = join(dir_path, 'blogs')

    all_story_files = [f for f in listdir(blog_path) if isfile(join(blog_path, f))]
    all_story_files.sort(key = lambda date: datetime.strptime(date[:-4], '%m-%d-%y'))
    
    for fileName in all_story_files:
        file_dir = join(blog_path, fileName)
        with open(file_dir) as file:
             lines = file.readlines()
             lines = [line.rstrip() for line in lines]
             story_obj = {'title' : fileName[:-4], 'paragraphs': lines}
             stories.append(story_obj)
    return render_template('bloglist.html', stories=stories)

@app.route('/dastory', methods=['GET'])
@jwt_required()
def story():
    story_num = request.args.get('story', default="Hello There", type=str)

    return render_template('blogindividual.html')

@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
    # for removing tokens
    res = make_response(redirect(url_for('signin')))
    unset_jwt_cookies(res)
    return res