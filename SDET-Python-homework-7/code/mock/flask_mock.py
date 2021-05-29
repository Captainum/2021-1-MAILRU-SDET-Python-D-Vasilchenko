import threading

from flask import Flask, json, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}


@app.route('/get_surname/<name>', methods=['GET'])
def get_user_surname(name):
    if surname := SURNAME_DATA.get(name):
        return jsonify([surname]), 200
    else:
        return jsonify([f'Surname for user {name} not found']), 404


@app.route('/add_surname', methods=['POST'])
def post_user_surname():
    data = request.json
    
    name = list(data.keys())[0]
    surname = data[name]

    if SURNAME_DATA.get(name):
        return jsonify([f'Name {name} already has a surname']), 406
    else:
        SURNAME_DATA[name] = surname
        return jsonify({name: surname}), 200


@app.route('/update_surname', methods=['PUT'])
def put_user_surname():
    data = request.json
    
    name = list(data.keys())[0]
    surname = data[name]

    if SURNAME_DATA.get(name):
        SURNAME_DATA[name] = surname
        return jsonify([f'Updated']), 200
    else:
        return jsonify([f'Surname for user {name} not found']), 404


@app.route('/delete_surname/<name>', methods=['DELETE'])
def delete_user_surname(name):
    if SURNAME_DATA.get(name):
        SURNAME_DATA.pop(name)
        return jsonify(['Deleted']), 200
    else:
        return jsonify([f'Surname for user {name} not found']), 404


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    server.start()
    return server


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify(f'OK, exiting'), 200