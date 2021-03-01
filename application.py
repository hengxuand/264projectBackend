from flask import Flask, jsonify, request, send_file
import json
import sqlite3
from datetime import datetime

application = Flask(__name__)


@application.route('/category', methods=['GET'])
def get_cat():
    with sqlite3.connect('foodorder.db') as conn:
        cur = conn.cursor()
        result = cur.execute("select * from category")
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/recommend', methods=['GET'])
def get_recommend():
    with sqlite3.connect('foodorder.db') as conn:
        cur = conn.cursor()
        result = cur.execute("select * from food where is_recommend = 1")
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/search/<keyword>', methods=['GET'])
def get_search_result(keyword):
    keyword = [keyword + "%"]
    with sqlite3.connect('foodorder.db') as conn:
        cur = conn.cursor()
        search_query = "select * from food where like(?, food_name) "
        result = cur.execute(search_query, keyword)
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/img/<img_name>', methods=['GET'])
def get_img(img_name):
    return send_file("img/" + img_name, mimetype='image/jpeg')


@application.route('/reg', methods=['POST'])
def reg_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        return jsonify(
            status='success',
            name=name,
            email=email,
            message="Welcome " + name
        )
    except Exception as e:
        return jsonify(
            status="fail",
            message="Wrong API",
            name="null",
            email="null")


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
