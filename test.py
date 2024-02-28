from flask import Flask
import requests 

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World! This is a basic Flask API.'

requests.get('')

if __name__ == '__main__':
    app.run(debug=True)
