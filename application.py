from flask import Flask, jsonify, request, send_file
import json
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

application = Flask(__name__)
key = b'sydDsHxGmjCj-E8Nz652hdJhLKU3D7N4TgPvz6x2qT8='
cipher = Fernet(key)
db = 'foodorder.db'
BAD_API = 'bad API request'


@application.route('/category', methods=['GET'])
def get_cat():
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        result = cur.execute("select * from category")
        items = [
            dict(zip([key[0] for key in cur.description], row))
            for row in result
        ]
        conn.commit()
        cur.close()
        return json.dumps(items)


@application.route('/categoryfoods/<category_id>', methods=['GET'])
def get_category_food(category_id):
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        result = cur.execute("select * from food where cat_id = ?",
                             (category_id, ))
        items = [
            dict(zip([key[0] for key in cur.description], row))
            for row in result
        ]
        conn.commit()
        cur.close()
        return json.dumps(items)


@application.route('/recommend', methods=['GET'])
def get_recommend():
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        result = cur.execute("select * from food where is_recommend = 1")
        items = [
            dict(zip([key[0] for key in cur.description], row))
            for row in result
        ]
        conn.commit()
        cur.close()
        return json.dumps(items)


@application.route('/search/<keyword>', methods=['GET'])
def get_search_result(keyword):
    # keyword = [keyword + "%"]
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        search_query = "select * from food where food_name like ?"
        result = cur.execute(search_query, ('%' + keyword+'%',))
        items = [
            dict(zip([key[0] for key in cur.description], row))
            for row in result
        ]
        print(items)
        conn.commit()
        cur.close()
        return json.dumps(items)


@application.route('/img/<img_name>', methods=['GET'])
def get_img(img_name):
    return send_file("img/" + img_name, mimetype='image/jpeg')


@application.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('userid')
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cart_result = cur.execute(
            "select * from food inner join (select food.food_id as f, quantity from cart inner join food where cart.user_id = ? and cart.food_id = food.food_id) where food.food_id = f",
            (user_id, ))
        items = [
            dict(zip([key[0] for key in cur.description], row))
            for row in cart_result
        ]
        print(items)
        conn.commit()
        cur.close()
        return json.dumps(items)


@application.route('/addToCart', methods=['POST'])
def add_to_cart():
    try:
        user_id = request.form['userid']
        food_id = request.form['foodid']
        print("adding: user_id: " + user_id + " food_id " + food_id)
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            result = cur.execute(
                "select * from cart where food_id = ? and user_id = ?",
                (food_id, user_id)).fetchall()
            if len(result) == 0:
                cur.execute(
                    "insert into cart (food_id, user_id, quantity) values (?, ?, ?)",
                    (food_id, user_id, 1))
            else:
                cur.execute(
                    "update cart set quantity = (SELECT quantity from cart where food_id = ? and user_id = ?) + 1 where food_id = ? and user_id = ?",
                    (food_id, user_id, food_id, user_id))
            conn.commit()
            cur.close()
        return jsonify(status='success', message='OK')

    except Exception as e:
        print(e)
        return jsonify(status='fail', message=BAD_API)


@application.route('/deleteFromCart', methods=['POST'])
def delete_from_cart():
    try:
        user_id = request.form['userid']
        food_id = request.form['foodid']
        print("deleting: user_id: " + user_id + " food_id " + food_id)
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            result = cur.execute(
                "select quantity from cart where food_id = ? and user_id = ?",
                (food_id, user_id)).fetchall()
            if result[0][0] == 1:
                cur.execute(
                    "delete from cart where food_id = ? and user_id = ?",
                    (food_id, user_id))
            else:
                cur.execute(
                    "update cart set quantity = (SELECT quantity from cart where food_id = ? and user_id = ?) - 1 where food_id = ? and user_id = ?",
                    (food_id, user_id, food_id, user_id))
            conn.commit()
            cur.close()
        return jsonify(status='success', message='OK')

    except Exception as e:
        print(e)
        return jsonify(status='fail', message=BAD_API)


@application.route('/orderpaid', methods=['POST'])
def order_paid():
    try:
        user_id = request.form['userid']
        payment_id = request.form['paymentid']
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            result = cur.execute(
                "SELECT * from cart where user_id = ?", (user_id, )).fetchall()
            print(result[0] + (payment_id,))
            for item in result:
                cur.execute(
                    "insert into order_food (food_id, user_id, quantity, payment_id) values (?,?,?,?)", item + (payment_id,))
            cur.execute("delete from cart where user_id = ?", (user_id,))
            conn.commit()
            cur.close()
            return jsonify(status='sucess', message='OK')

    except Exception as e:
        print(e)
        return jsonify(status='fail', message=BAD_API)


@application.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            login_query = "select * from user where email = ?"
            result = cur.execute(login_query, (email, )).fetchall()
            if len(result) == 1:
                user = result[0]
                if password == cipher.decrypt(user[1]).decode():
                    user_id = user[0]

                    cart_result = cur.execute(
                        "select * from food inner join (select food.food_id as f, quantity from cart inner join food where cart.user_id = ? and cart.food_id = food.food_id) where food.food_id = f",
                        (user_id, ))

                    items = [
                        dict(zip([key[0] for key in cur.description], row))
                        for row in cart_result
                    ]
                    conn.commit()
                    cur.close()
                    return jsonify(status='success',
                                   message='welcome',
                                   userId=user[0],
                                   name=user[2],
                                   email=user[3],
                                   phoneNumber=user[4],
                                   cart=json.dumps(items))
                else:
                    conn.commit()
                    cur.close()
                    return jsonify(status='fail', message='wrong password')
            else:
                conn.commit()
                cur.close()
                return jsonify(status='fail', message='not existing email')

    except Exception as e:
        print(e)
        return jsonify(status='fail', message=BAD_API)


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
            result = cur.execute(check_query, (email, )).fetchall()
            if len(result) > 0:
                print("email already exists! return status exists")
                conn.commit()
                cur.close()
                return jsonify(status="exists",
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
                    "select user_id from user where email = ?",
                    (email, )).fetchone()[0]
                conn.commit()
                cur.close()
                return jsonify(status='success',
                               userId=user_id,
                               name=name,
                               email=email,
                               phoneNumber=phone,
                               message="Welcome " + name)

    except Exception as e:
        print(e)
        return jsonify(status="fail",
                       message=BAD_API,
                       name="null",
                       phoneNumber='null',
                       email="null")


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
