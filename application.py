from flask import Flask, jsonify, request
#import json
#import sqlite3

application = Flask(__name__)


@application.route('/', methods=['GET'])
def home():
    return '<h1> API demo </h1>'


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
