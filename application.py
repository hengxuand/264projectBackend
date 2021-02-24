from flask import Flask, jsonify, request, send_file
import json
import sqlite3

application = Flask(__name__)


@application.route('/category', methods=['GET'])
def get_cat():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        result = cur.execute("select * from category")
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/recommend', methods=['GET'])
def get_recommend():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        result = cur.execute("select * from food where is_recommend = 1")
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/img/<img_name>', methods=['GET'])
def get_img(img_name):
    return send_file("img/" + img_name, mimetype='image/jpeg')


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
