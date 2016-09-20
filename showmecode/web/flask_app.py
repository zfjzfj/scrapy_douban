from flask import Flask
from flask import Response
flask_app = Flask('flaskapp')


@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )
# flask_app.run(host='0.0.0.0',debug=True)
app = flask_app.wsgi_app

app = flask_app
