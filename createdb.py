import sqlite3

conn = sqlite3.connect('foodorder.db')
cur = conn.cursor()


cur.execute(
    "create table category(cat_id INTEGER PRIMARY KEY, cat_name TEXT, cat_img TEXT)"
)
cur.execute(
    "CREATE TABLE food(food_id INTEGER PRIMARY KEY, food_name TEXT, food_description TEXT, food_price REAL, food_img TEXT, cat_id INTEGER, is_recommend INTEGER DEFAULT 0, FOREIGN KEY (cat_id) REFERENCES category (cat_id))"
)

cur.execute("create table payment(payment_id INTEGER PRIMARY KEY, card_num TEXT, name TEXT, exp TEXT, cvv INTEGER)")

cur.execute("create table order_table(order_id INTEGER PRIMARY KEY, is_paid INTEGER DEFAULT 0, name TEXT, time DATETIME)")

cur.execute(
    "create table order_food(food_id INTEGER, order_id INTEGER, quantity INTEGER, FOREIGN KEY (food_id) REFERENCES food (food_id), FOREIGN KEY (order_id) REFERENCES order_table (order_id))"
)

cur.execute("create table user(user_id INTEGER PRIMARY KEY, password TEXT, name TEXT, email TEXT, phone_number TEXT, reg_time timestamp)")

conn.commit()
cur.close()
