import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

conn = sqlite3.connect('foodorder.db')
cur = conn.cursor()


cur.execute(
    "create table category(cat_id INTEGER PRIMARY KEY, cat_name TEXT, cat_img TEXT)"
)
cur.execute(
    "CREATE TABLE food(food_id INTEGER PRIMARY KEY, food_name TEXT, food_description TEXT, food_price REAL, food_img TEXT, cat_id INTEGER, is_recommend INTEGER DEFAULT 0, FOREIGN KEY (cat_id) REFERENCES category (cat_id))"
)

cur.execute("create table payment(payment_id INTEGER PRIMARY KEY, card_num TEXT, name TEXT, cvv INTEGER, exp TEXT)")

cur.execute("create table order_table(order_id INTEGER PRIMARY KEY, payment_id INTEGER DEFAULT null, user_id TEXT, total_price REAL)")

cur.execute(
    "create table order_food(food_id INTEGER, order_id INTEGER, quantity INTEGER, FOREIGN KEY (food_id) REFERENCES food (food_id), FOREIGN KEY (order_id) REFERENCES order_table (order_id))")

cur.execute("create table user(user_id INTEGER PRIMARY KEY, password TEXT, name TEXT, email TEXT, phone_number TEXT, reg_time timestamp)")


'''
insert category table
update category set cat_img = 'img/noodlecat.jpeg' where cat_id = 1
'''

cat_query = "insert into category (cat_name, cat_img) values (?, ?)"
cur.execute(cat_query, ("Appetizers", "img/appetizerscat.jpeg"))
cur.execute(cat_query, ("Salads", "img/saladscat.jpeg"))
cur.execute(cat_query, ("Noodles", "img/noodlescat.jpeg"))
cur.execute(cat_query, ("Rice", "img/ricecat.jpeg"))
cur.execute(cat_query, ("Vermicelli", "img/vermicellicat.jpeg"))
cur.execute(cat_query, ("Kids", "img/kidscat.jpeg"))
cur.execute(cat_query, ("Stir Fry", "img/stirfrycat.jpeg"))
cur.execute(cat_query, ("Specials", "img/specialscat.jpeg"))
cur.execute(cat_query, ("Drinks", "img/drinkscat.jpeg"))

food_query = "insert into food (food_name, food_description, food_price, food_img, cat_id, is_recommend) values (?,?,?,?,?,?)"
cur.execute(food_query, ("Pho", "Rice noodle",
                         9.89, "img/phorecommend.jpeg", 3, 1))
cur.execute(food_query, ("Spring Roll",
                         "meat wrap with rice paper", 7.77, "img/springrollrecommend.jpeg", 1, 1))
cur.execute(food_query, ("Shaking Beef",
                         "beef cut into small cubes", 15.55, "img/shakingbeefrecommend.jpeg", 2, 1))
cur.execute(food_query, ("Egg Roll",
                         "meat wrap with fried rice paper", 7.89, "img/eggrollrecommend.jpeg", 1, 0))
cur.execute(food_query, ("Hue noodle",
                         "Spicy beef noodle soup", 10.11, "img/huerecommend.jpeg", 8, 1))


key = b'sydDsHxGmjCj-E8Nz652hdJhLKU3D7N4TgPvz6x2qT8='
cipher = Fernet(key)

user_query = "insert into user (name,password, email, phone_number, reg_time) values (?,?,?,?,?)"
cur.execute(user_query, ("nina", cipher.encrypt('nina112194'.encode()), "nina@gmail.com",
                         "7149025986", datetime.now()))

conn.commit()
cur.close()
