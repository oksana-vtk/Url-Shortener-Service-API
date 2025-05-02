import mysql.connector
from dotenv import load_dotenv
import os


# завантаження змінних з .env
load_dotenv()


# Підключення до бази даних
def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME_SHORTENER")
    )


def insert_into_table_urls(val):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " INSERT INTO urls(url, short_part, short_url) " \
          " VALUES (%s, %s, %s) "
    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return val


def insert_into_table_urls_for_user_and_sku(val):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " INSERT INTO urls(url, user_id, variation_sku_id, short_part, short_url) " \
          " VALUES (%s, %s, %s, %s, %s) "
    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return val


def find_all_short_parts():
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT short_part " \
          " FROM urls "

    mycursor.execute(sql)
    all_short_parts = mycursor.fetchall()

    for i in range(len(all_short_parts)):
        a = all_short_parts[i]
        (all_short_parts[i],) = a  # unpack tuple

    mycursor.close()
    mydb.close()

    return all_short_parts


def find_all_urls():
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT url " \
          " FROM urls " \
          " WHERE user_id = '0' AND variation_sku_id = '0' "

    mycursor.execute(sql)
    all_urls = mycursor.fetchall()

    for i in range(len(all_urls)):
        a = all_urls[i]
        (all_urls[i],) = a  # unpack tuple

    #print(all_urls)

    return all_urls


def find_all_urls_by_user_and_sku(val):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT url " \
          " FROM urls " \
          " WHERE user_id = %s AND variation_sku_id = %s "

    mycursor.execute(sql, val)
    all_urls_by_user_and_sku = mycursor.fetchall()

    for i in range(len(all_urls_by_user_and_sku)):
        a = all_urls_by_user_and_sku[i]
        (all_urls_by_user_and_sku[i],) = a  # unpack tuple

    #print(all_urls)

    return all_urls_by_user_and_sku


def find_short_part(url):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT short_part " \
          " FROM urls " \
          " WHERE url = %s AND user_id = '0' AND variation_sku_id = '0' "
    val = url

    mycursor.execute(sql, val)
    short_part = mycursor.fetchone()

    a = short_part
    (short_part,) = a  # unpack tuple

    mycursor.close()
    mydb.close()

    return short_part


def find_short_part_for_user_and_sku(val):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT short_part " \
          " FROM urls " \
          " WHERE url = %s AND user_id = %s AND variation_sku_id = %s"
    mycursor.execute(sql, val)
    short_part_for_user_and_sku = mycursor.fetchone()

    a = short_part_for_user_and_sku
    (short_part_for_user_and_sku,) = a  # unpack tuple

    mycursor.close()
    mydb.close()

    return short_part_for_user_and_sku


def find_short_url(short_part):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT short_url " \
          " FROM urls " \
          " WHERE short_part = %s "
    val = short_part

    mycursor.execute(sql, val)
    short_url = mycursor.fetchone()

    a = short_url
    (short_url,) = a  # unpack tuple

    mycursor.close()
    mydb.close()

    return short_url


def find_url(short_part):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT url " \
          " FROM urls " \
          " WHERE short_part = %s "
    val = short_part

    mycursor.execute(sql, val)
    url = mycursor.fetchone()

    a = url
    (url,) = a  # unpack tuple

    mycursor.close()
    mydb.close()

    return url


def update_redirect_clicks(short_part):
    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " UPDATE urls" \
          " SET redirect_clicks = redirect_clicks + 1, last_click = current_timestamp() " \
          " WHERE short_part = %s "
    val = short_part

    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return short_part

