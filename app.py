from datetime import datetime, timedelta
from functools import wraps
from random import random, randint

import jwt
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
        data = jwt.decode(request.args.get('jwt'), app.config['SECRET_KEY'])
        if str(data['code']) == code:
            authorised = True

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
def newEntry():
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
    code = request.form['code']

    selectEntries = 'SELECT passphrase FROM lists WHERE id=(%s)'
    cursor.execute(selectEntries, listId)
    data = cursor.fetchone()

    if data[0] == passphrase:
        message = "Correct passphrase"
        token = get_token(code)
        json = jsonify({'message': message,
                        'token': str(token)})
        json.set_cookie('jwt', token, domain='127.0.0.1')
        return json
    else:
        message = "Incorrect passphrase"

    return jsonify({'message': message})


@app.route('/deleteEntry', methods=['DELETE'])
def delete_entry() :
    entryId = request.args.get('id')
    print(entryId)
    delete_statement = 'DELETE FROM list_entries WHERE id=%s'
    cursor.execute(delete_statement, entryId)
    conn.commit()

    return ""


def generate_code():
    cursor.execute('SELECT code FROM lists')
    data = cursor.fetchall()
    code = randint(1000, 9999)
    while data.__contains__(code):
        code = randint(1000, 9999)

    return code


def get_token(code):
    token = jwt.encode({'code': code, 'exp': datetime.utcnow() + timedelta(minutes=15)},
                       app.config['SECRET_KEY'])
    return token


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=5035, debug=True)
