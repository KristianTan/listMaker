from random import random, randint

from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'kristian.tan'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kkttkktt98'
app.config['MYSQL_DATABASE_DB'] = 'kristiantan_RESTService'
app.config['MYSQL_DATABASE_HOST'] = 'cs2s.yorkdc.net'

mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/createList', methods=['GET', 'POST'])
def sendData():
    title = request.form['title']
    passphrase = request.form['passphrase']
    code = generateCode()

    insert = 'INSERT INTO lists(title, code, passphrase) VALUES (%s, %s, %s)'
    cursor.execute(insert, (title, code, passphrase))
    conn.commit()

    return jsonify({'code': code})


@app.route('/getList', methods=['GET'])
def getList():
    code = request.args.get('code')
    selectList = 'SELECT * FROM lists WHERE code=(%s)'
    cursor.execute(selectList, code)
    listData = cursor.fetchone()

    if listData == None:
        return jsonify({'message': 'No list found for that code',
                        'code': code})

    id = listData[0]
    title = listData[1]
    code = listData[2]

    selectEntries = 'SELECT content FROM list_entries WHERE listid=(%s)'
    cursor.execute(selectEntries, id)
    entries = [item[0] for item in cursor.fetchall()]

    return jsonify({'message': 'New list created',
                    'id': id,
                    'title': title,
                    'code': code,
                    'entries': entries})


@app.route('/newEntry', methods=['POST'])
def newEntry():
    listId = request.form['listId']
    text = request.form['text']

    insert = 'INSERT INTO list_entries(listid, content) VALUES (%s, %s)'
    cursor.execute(insert, (listId, text))
    conn.commit()

    return jsonify()


def generateCode():
    cursor.execute('SELECT code FROM lists')
    data = cursor.fetchall()
    code = randint(1000, 9999)
    while data.__contains__(code):
        code = randint(1000, 9999)

    return code


if __name__ == '__main__':
    app.run()
