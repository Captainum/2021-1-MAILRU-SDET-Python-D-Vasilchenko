#import threading

from flask import Flask, json, jsonify, request

MOCK_HOST = '0.0.0.0'
MOCK_PORT = '8083'

app = Flask(__name__)

USERNAME_DATA = {'test_username': "whewrwerw"}

@app.route('/vk_id/<username>', methods=['GET'])
def get_username(username):
    if username in USERNAME_DATA:
        return jsonify({'vk_id': USERNAME_DATA[username]}), 200
    else:
        return jsonify({}), 404


@app.route('/add_username', methods=['POST'])
def add_username():
    data = json.loads(request.data)
    username = data['username']
    vk_id = data['vk_id']

    USERNAME_DATA[username] = vk_id

    return jsonify('OK'), 201


@app.route('/delete_username/<username>', methods=['POST'])
def delete_username(username):
    USERNAME_DATA.pop(username)
    return jsonify('OK'), 204


@app.route('/update_username', methods=['PUT'])
def update_username():
    data = json.loads(request.data)
    username = data['username']
    vk_id = data['vk_id']

    USERNAME_DATA[username] = vk_id

    return jsonify('OK'), 200


def shutdown_mock():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_mock()
    return jsonify('OK, exiting'), 200


if __name__ == '__main__':
    app.run(host=MOCK_HOST, port=MOCK_PORT)