from flask import Flask, jsonify
import os
from version import __version__

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

port = int(os.getenv('PORT', 8080))
application_path = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/status')
def app_stauts():
    # return app version
    return jsonify(application="Yousights-FE", version=__version__)


@app.route('/logs')
def get_logs(self):
    file_path = application_path + "/logs/server.log"
    with open(file_path) as file:
        logs = file.readlines()
    return jsonify(application="Yousights-FE", logs=logs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
