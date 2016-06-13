from flask.ext.api import FlaskAPI
from flask import request, current_app, abort
from functools import wraps

app = FlaskAPI(__name__)
app.config.from_object('settings')


def token_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-TOKEN', None) != current_app.config['API_TOKEN']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/score', methods=['POST'])
@token_auth
def score():
    from engine import content_engine
    item = request.data.get('item')
    num_scores = request.data.get('num', 10)
    if not item:
        return []
    return content_engine.score(str(item), num_scores)


@app.route('/train')
@token_auth
def train():
    from engines import content_engine
    data_url = request.data.get('data-url', None)
    content_engine.train(data_url)
    return {"message": "It Works!", "success": 1}


if __name__ == '__main__':
    app.debug = True
    app.run()
