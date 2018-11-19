from flask import Flask

app = Flask(__name__)


if __name__ == '__main__':  # Only will run if the code is execute inside the python interpreter
    app.secret_key = 'super_secret_key'
    app.debug = True
    #app.run(host='0.0.0.0', port = 5000, ssl_context=('cert.pem', 'key.pem'))
    app.run(host='0.0.0.0', port=5000)
