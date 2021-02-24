import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()


cur.execute(
    "create table category(cat_id INTEGER PRIMARY KEY, cat_name TEXT)"
)
cur.execute(
    "CREATE TABLE food(food_id INTEGER PRIMARY KEY, name TEXT, description TEXT, price INTEGER, imgurl TEXT, cat_id INTEGER, FOREIGN KEY (cat_id) REFERENCES category (cat_id))"
)

cur.execute("create table payment(payment_id INTEGER PRIMARY KEY, card_num TEXT, name TEXT, exp TEXT, cvv INTEGER)")

cur.execute("create table order_table(order_id INTEGER PRIMARY KEY, is_paid INTEGER DEFAULT 0, name TEXT, time DATETIME)")

cur.execute(
    "create table order_food(food_id INTEGER, order_id INTEGER, quantity INTEGER, FOREIGN KEY (food_id) REFERENCES food (food_id), FOREIGN KEY (order_id) REFERENCES order_table (order_id))"
)

conn.commit()
cur.close()
