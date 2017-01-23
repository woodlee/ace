import ace
import flask


app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # Extremely rudimentary DOS protection


@app.route('/parse', methods=['POST'])
def parse_endpoint():
    message = flask.request.form.get('message')
    if message is None:
        flask.abort(400, 'Please provide a "message" parameter')
    return flask.jsonify(**ace.parsing.parse_message(message))
