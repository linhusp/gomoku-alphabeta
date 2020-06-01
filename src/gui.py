from flask import (
    request,
    Flask,
    render_template
)
from game import GameRunner
import json

app = Flask(__name__)
game_runner = GameRunner()


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/restart', methods=['GET'])
def restart():
    player_index = int(request.args['playerIndex'])
    if player_index not in [-1, 1]:
        status = 'Fail'
    else:
        status = 'OK'
        game_runner.restart(player_index)
    return json.dumps({'status': status})


@app.route('/play')
def play():
    x, y = request.args['x'], request.args['y']
    if game_runner.play(int(x), int(y)):
        status = 'OK'
    else:
        status = 'Fail'
    return json.dumps({'status': status, 'game_status': game_runner.get_status()})


@app.route('/aiplay')
def aiplay():
    status, move = game_runner.aiplay()
    if status:
        return json.dumps(
            {
                'status': 'OK',
                'move': {'x': int(move[0]), 'y': int(move[1])},
                'game_status': game_runner.get_status()
            }
        )
    return json.dumps({'status': 'Fail', 'game_status': game_runner.get_status()})


@app.route('/get_gamestate')
def get_gamestate():
    return json.dumps({'status': 'OK', 'game_status': game_runner.get_status()})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


def main():
    pass


if __name__ == "__main__":
    app.run(debug=True)
