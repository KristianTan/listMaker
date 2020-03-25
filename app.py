from flask import Flask, request, jsonify

app = Flask(__name__)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/sendData', methods=['GET', 'POST'])
def sendData():
    title = request.form['title']
    passphrase = request.form['passphrase']
    output = title + ", " + passphrase
    return jsonify({'output': output})


if __name__ == '__main__':
    app.run()
