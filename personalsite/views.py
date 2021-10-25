from encrypt import encrypt_files
from personalsite import app, jwt
from flask import render_template, make_response, url_for, send_file, abort, flash, request, redirect, jsonify, Response
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, set_access_cookies, unset_jwt_cookies
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
from cryptography.fernet import Fernet
from personalsite.decrypt import decrypt_file

ENCRYPTIONKEY = ''
USERNAME = ''
PASSWORD = ''

try:
    import secret
    USERNAME = secret.USERNAME
    PASSWORD = secret.PASSWORD
    ENCRYPTIONKEY = secret.ENCRYPTIONKEY
except:
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    ENCRYPTIONKEY = os.environ['ENCRYPTIONKEY']

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
        if username != USERNAME or password != PASSWORD:
            return 'incorrect username'

        additional_claims = {'jwt':'some audience', 'hello':'there'}

        # create res to set cookie and redirect to blog
        response = make_response(redirect(url_for('blog')), 302) # 302 is the status code for redirect https://stackoverflow.com/questions/47464961/flask-routing-problems
        response.headers['Access-Control-Allow-Origin'] = '*'
        access_token = create_access_token(identity=username, additional_claims=additional_claims)
        set_access_cookies(response, access_token)

        return response


@app.route('/dastoryhub', methods=['GET'])
@jwt_required()     # https://flask-jwt-extended.readthedocs.io/en/stable/_modules/flask_jwt_extended/view_decorators/#jwt_required
                    # The wrap() provided by python is good for defining wrapper functions. helps preserve the meta data (__name__) of the original function.
def blog():
    '''
        metadata: 
            all blog files with display date first in format %d-%m-%y where all will take up two char
            blog file will be .txt files
            each paragraph belongs on one line
    '''
    stories = []

    data_claim = get_jwt()
    claims = jsonify(hello=data_claim['hello'])

    dir_path = os.path.dirname(os.path.realpath(__file__))
    blog_path = join(dir_path, 'blogs')

    all_story_files = [f for f in listdir(blog_path) if isfile(join(blog_path, f))]
    all_story_files.sort(key = lambda date: datetime.strptime(date[0:8], '%m-%d-%y'), reverse=True) # sort stories

    for fileName in all_story_files:
        file_dir = join(blog_path, fileName)

        with open(file_dir) as file:
            encrypted = file.read()

        lines = decrypt_file(encrypted, ENCRYPTIONKEY)
        
        story_obj = {'title' : fileName[:-4], 'paragraphs': lines}
        stories.append(story_obj)

    return render_template('bloglist.html', stories=stories)

@app.route('/dastory', methods=['GET'])
@jwt_required()
def story():
    story_title = request.args.get('story', default="Hello There", type=str)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    blog_path = join(dir_path, 'blogs')

    story_path = join(blog_path, story_title+'.txt')

    story = {}

    with open(story_path) as file:
        encrypted = file.read()

    lines = decrypt_file(encrypted, ENCRYPTIONKEY)
    
    story_obj = {'title' : story_title, 'paragraphs': lines}
    story = story_obj

    return render_template('blogindividual.html', story=story)

@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
    # for removing tokens
    res = make_response(redirect(url_for('signin')))
    unset_jwt_cookies(res)
    return res