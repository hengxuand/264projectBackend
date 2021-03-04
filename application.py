from flask import Flask, jsonify, request, send_file
import json
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

application = Flask(__name__)
key = b'sydDsHxGmjCj-E8Nz652hdJhLKU3D7N4TgPvz6x2qT8='
cipher = Fernet(key)
db = 'foodorder.db'


@application.route('/category', methods=['GET'])
def get_cat():
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        result = cur.execute("select * from category")
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/categoryfoods/<category_id>', methods=['GET'])
def get_category_food(category_id):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        result = cur.execute(
            "select * from food where cat_id = ?", (category_id,))
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/recommend', methods=['GET'])
def get_recommend():
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        result = cur.execute("select * from food where is_recommend = 1")
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/search/<keyword>', methods=['GET'])
def get_search_result(keyword):
    keyword = [keyword + "%"]
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        search_query = "select * from food where like(?, food_name) "
        result = cur.execute(search_query, keyword)
        items = [dict(zip([key[0] for key in cur.description], row))
                 for row in result]
        return json.dumps(items)


@application.route('/img/<img_name>', methods=['GET'])
def get_img(img_name):
    return send_file("img/" + img_name, mimetype='image/jpeg')


@application.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            login_query = "select * from user where email = ?"
            result = cur.execute(login_query, (email,)).fetchall()
            print(result)
            if len(result) == 1:
                user = result[0]
                if password == cipher.decrypt(user[1]).decode():
                    return jsonify(
                        status='success',
                        message='welcome',
                        userId=user[0],
                        name=user[2],
                        email=user[3],
                        phoneNumber=user[4]
                    )
                else:
                    return jsonify(
                        status='fail',
                        message='wrong password'
                    )
            else:
                return jsonify(
                    status='fail',
                    message='not existing email'
                )

    except Exception as e:
        print(e)
        return jsonify(
            status='fail',
            message='bad API request'
        )


@application.route('/reg', methods=['POST'])
def reg_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        with sqlite3.connect(db) as conn:
            cur = conn.cursor()

            check_query = "select * from user where email = ?"
            result = cur.execute(check_query, (email,)).fetchall()
            if len(result) > 0:
                print("email already exists! return status exists")
                return jsonify(
                    status="exists",
                    message="Existing email",
                    name=name,
                    phoneNumber=phone,
                    email=email)
            elif len(result) == 0:
                print('email is good to go')
                user_query = "insert into user (name, password, email, phone_number, reg_time) values (?,?,?,?,?)"
                cur.execute(user_query, (name, cipher.encrypt(
                    password.encode()), email, phone, datetime.now()))
                conn.commit()
                user_id = cur.execute(
                    "select user_id from user where email = ?", (email,)).fetchone()[0]

                return jsonify(
                    status='success',
                    userId=user_id,
                    name=name,
                    email=email,
                    phoneNumber=phone,
                    message="Welcome " + name
                )

    except Exception as e:
        print(e)
        return jsonify(
            status="fail",
            message="Bad API Request",
            name="null",
            phoneNumber='null',
            email="null")


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0', port=5000)
