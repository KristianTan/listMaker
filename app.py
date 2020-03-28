from datetime import datetime, timedelta
from functools import wraps
from random import random, randint

import binascii
import hashlib
import jwt
import os
from flask import Flask, request, jsonify, make_response, session
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'kristian.tan'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kkttkktt98'
app.config['MYSQL_DATABASE_DB'] = 'kristiantan_RESTService'
app.config['MYSQL_DATABASE_HOST'] = 'cs2s.yorkdc.net'
app.config['SECRET_KEY'] = 'secret'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/createList', methods=['GET', 'POST'])
def create_list():
    title = request.form['title']
    passphrase = request.form['passphrase']
    code = generate_code()
    jwt = get_token(code)

    insert = 'INSERT INTO lists(title, code, passphrase) VALUES (%s, %s, %s)'
    cursor.execute(insert, (title, code, passphrase))
    conn.commit()

    return jsonify({'code': code,
                    'jwt': jwt})


@app.route('/getList', methods=['GET'])
def get_list():
    code = request.args.get('code')
    selectList = 'SELECT * FROM lists WHERE code=(%s)'
    cursor.execute(selectList, code)
    listData = cursor.fetchone()

    if listData == None:
        return jsonify({'message': 'No list found for that code',
                        'code': code})

    authorised = False
    if request.args.get('jwt'):
        try:
            data = jwt.decode(request.args.get('jwt'), app.config['SECRET_KEY'])
            # Check if user is list member
            username = data['user']

            select_users = 'SELECT id FROM users WHERE username=(%s)'
            cursor.execute(select_users, username)
            user_id = cursor.fetchone()

            select_lists = 'SELECT id FROM lists WHERE code=(%s)'
            cursor.execute(select_lists, code)
            list_id = cursor.fetchone()

            check_list_member = 'SELECT * FROM list_members WHERE user_id=%s AND list_id=%s'
            cursor.execute(check_list_member, (user_id[0], list_id[0]))
            result = cursor.fetchone()
            if result is not None:
                authorised = True
        except jwt.ExpiredSignatureError:
            pass

    id = listData[0]
    title = listData[1]
    code = listData[2]

    selectEntries = 'SELECT content, id FROM list_entries WHERE listid=(%s)'
    cursor.execute(selectEntries, id)
    # entries = [item[0] for item in cursor.fetchall()]
    columns = [column[0] for column in cursor.description]
    entries = []

    for row in cursor.fetchall():
        entries.append(dict(zip(columns, row)))

    return jsonify({'message': 'List found',
                    'id': id,
                    'title': title,
                    'code': code,
                    'entries': entries,
                    'auth': authorised})


@app.route('/newEntry', methods=['POST'])
def new_entry():
    listId = request.form['listId']
    text = request.form['text']

    insert = 'INSERT INTO list_entries(listid, content) VALUES (%s, %s)'
    cursor.execute(insert, (listId, text))
    conn.commit()

    return jsonify()


@app.route('/checkPassphrase', methods=['POST'])
def check_passphrase():
    passphrase = request.form['passPhrase']
    listId = request.form['listId']
    # code = request.form['code']
    jwt_token = request.form['jwt']

    selectEntries = 'SELECT passphrase FROM lists WHERE id=(%s)'
    cursor.execute(selectEntries, listId)
    data = cursor.fetchone()

    if data[0] == passphrase:
        if jwt_token is not None:
            print("JWT: " + str(jwt_token))
            save_list(listId, jwt_token)
        return jsonify({'message': "Correct passphrase"})
    else:
        message = "Incorrect passphrase"

    return jsonify({'message': message})


@app.route('/deleteEntry', methods=['DELETE'])
def delete_entry():
    entryId = request.args.get('id')
    delete_statement = 'DELETE FROM list_entries WHERE id=%s'
    cursor.execute(delete_statement, entryId)
    conn.commit()

    return ""


@app.route('/renameList', methods=['PUT'])
def rename_list():
    listId = request.form['listId']
    title = request.form['newTitle']

    update_statement = 'UPDATE lists SET title=(%s) WHERE id=(%s)'
    cursor.execute(update_statement, (title, listId))
    conn.commit()

    return ""


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']

    select_users = 'SELECT * FROM users WHERE username=(%s)'
    cursor.execute(select_users, username)
    data = cursor.fetchone()

    if data is not None:
        return jsonify({'message': 'User already exists with that username'})

    if password != confirmPassword:
        return jsonify({'message': 'Passwords do not match'})

    password_hash = hash_password(password)
    jwt = get_token(username)

    insert = 'INSERT INTO users(username, password) VALUES (%s, %s)'
    cursor.execute(insert, (username, password_hash))
    conn.commit()

    return jsonify({
        'jwt': jwt
    })


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    select_users = 'SELECT * FROM users WHERE username=(%s)'
    cursor.execute(select_users, username)
    data = cursor.fetchone()

    if data is None:
        return jsonify({'message': 'No user found with that username'})

    if not verify_password(data[2], password):
        return jsonify({'message': 'Incorrect password'})

    jwt = get_token(username)

    return jsonify({
        'jwt': jwt
    })


# @app.route('/saveList', methods=['POST'])
def save_list(list_id, jwt_code):
    # list_id = request.form['listId']
    data = jwt.decode(jwt_code, app.config['SECRET_KEY'])
    username = data['user']

    select_users = 'SELECT * FROM users WHERE username=(%s)'
    cursor.execute(select_users, username)
    user = cursor.fetchone()

    check_list_member = 'SELECT * FROM list_members WHERE user_id=%s AND list_id=%s'
    cursor.execute(check_list_member, (user[0], list_id))
    result = cursor.fetchone()

    if result is None:
        insert_statement = 'INSERT INTO list_members (list_id, user_id) VALUES (%s, %s)'
        cursor.execute(insert_statement, (list_id, user[0]))
        conn.commit()
    return jsonify({'message': 'List saved'})


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def generate_code():
    cursor.execute('SELECT code FROM lists')
    data = cursor.fetchall()
    code = randint(1000, 9999)
    while data.__contains__(code):
        code = randint(1000, 9999)

    return code


def get_token(username):
    return jwt.encode({'user': username},
                      app.config['SECRET_KEY'])


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5035, debug=True)
