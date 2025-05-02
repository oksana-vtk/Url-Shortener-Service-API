from flask import Flask, request, redirect
from flask_caching import Cache
import string
import random
import re
from datetime import datetime
from dotenv import load_dotenv
import os
import url_shortener_sql as sql


app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# Generate a random string of 6 characters.
def generate_random_string():

    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(characters, k=6))

    return random_string


# API_1: Документація в файлі API_DOC.md
# Генерація короткого посилання по заданому посиланню
@app.route("/url-shortener", methods=["POST"])
def url_shortener():

    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open("logs.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"\n\n{current_datetime} Url_shortener process: \n")

    user_data = request.get_json()

    url = user_data["url"]

    url_pattern = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
    r = re.compile(url_pattern)

    # завантаження змінних з .env
    load_dotenv()

    # завантажуємо домен із середовища .env
    domain = os.getenv("MY_DOMAIN")

    # якщо url відповідає паттерну url_pattern (тобто це справжній url)
    if re.findall(r, url):

        # якщо передається user_id і variation_sku_id
        if list(user_data.keys()).count("user_id") == 1 and list(user_data.keys()).count("variation_sku_id") == 1:

            user_id = user_data["user_id"]
            sku = user_data["variation_sku_id"]

            # якщо url вже існує в базі даних для даного користувача та товару (відповідно, для нього вже є short_part)
            if url in sql.find_all_urls_by_user_and_sku([user_id, sku]):

                # знаходимо існуючу short_part
                short_part = sql.find_short_part_for_user_and_sku([url, user_id, sku])

                # знаходимо існуючий short_url
                short_url = sql.find_short_url([short_part])

                result = {"url": url, "user_id": user_id, "variation_sku_id": sku,
                          "short_part": short_part, "short_url": short_url,
                          "status": {"code": 2001,
                                     "message": "Url already exists for this user and variation_sku_id. "
                                                "Short_part is from database without new short_part generation."}}
                print(result)
                with open("logs.log", "a", encoding="utf-8") as log_file:
                    log_file.write(str(result))

                return result

            # якщо url для конкретного користувача user_id і sku не існує в базі даних
            else:
                # генеруємо нову short_part
                short_part = generate_random_string()

                # якщо ця згенерована short_part випадково співпала з вже існуючою послідовністю в базі даних, то генеруємо нову
                # послідовність, до поки ця згенерована послідовність не стане унікальною
                while short_part in sql.find_all_short_parts():
                    short_part = generate_random_string()
                    # print("new short part", short_part)

                # як тільки short_part стала унікальною, то створюємо short_url
                short_url = domain + short_part

                # вставляємо всі дані в базу даних в таблицю urls
                sql.insert_into_table_urls_for_user_and_sku([url, user_id, sku, short_part, short_url])

                result = {"url": url, "user_id": user_id, "variation_sku_id": sku,
                          "short_part": short_part, "short_url": short_url,
                          "status": {"code": 2002,
                                     "message": "New short_part was generated successfully for this user and variation_sku_id. "
                                                "Url, short_part and short_url was added to database successfully."}}
                print(result)
                with open("logs.log", "a", encoding="utf-8") as log_file:
                    log_file.write(str(result))

                return result

        # якщо передається тільки user_id
        elif list(user_data.keys()).count("user_id") == 1 and list(user_data.keys()).count("variation_sku_id") == 0:

            result_error = {"url": url,
                            "user_id": user_data["user_id"],
                            "variation_sku_id": None,
                            "status": {"code": 4002,
                                       "message": "Please input variation_sku_id."}}
            print(result_error)
            with open("logs.log", "a", encoding="utf-8") as log_file:
                log_file.write(str(result_error))

            return result_error

        # якщо передається тільки variation_sku_id
        elif list(user_data.keys()).count("user_id") == 0 and list(user_data.keys()).count("variation_sku_id") == 1:

            result_error = {"url": url,
                            "user_id": None,
                            "variation_sku_id": user_data["variation_sku_id"],
                            "status": {"code": 4003,
                                       "message": "Please input user_id."}}
            print(result_error)
            with open("logs.log", "a", encoding="utf-8") as log_file:
                log_file.write(str(result_error))

            return result_error

        # якщо передається тільки url
        else:

            # якщо url вже існує в базі даних (виключаючи url для вказаних user_id і variation_sku_id)
            if url in sql.find_all_urls():

                # знаходимо існуючу short_part для всіх url, де user_id = '0' AND variation_sku_id = '0'
                short_part = sql.find_short_part([url])

                # знаходимо існуючий short_url
                short_url = sql.find_short_url([short_part])

                result = {"url": url, "short_part": short_part, "short_url": short_url,
                          "status": {"code": 2003,
                                     "message": "Url already exists. "
                                                "Short_part is from database without new short_part generation."}}
                print(result)
                with open("logs.log", "a", encoding="utf-8") as log_file:
                    log_file.write(str(result))

                return result

            # якщо url не існує в базі даних
            else:
                # генеруємо нову short_part
                short_part = generate_random_string()

                # якщо ця згенерована short_part випадково співпала з вже існуючою послідовністю в базі даних, то генеруємо нову
                # послідовність, до поки ця згенерована послідовність не стане унікальною
                while short_part in sql.find_all_short_parts():
                    short_part = generate_random_string()
                    # print("new short part", short_part)

                # як тільки short_part стала унікальною, то створюємо short_url
                short_url = domain + short_part

                # вставляємо дані в базу даних
                sql.insert_into_table_urls([url, short_part, short_url])

                result = {"url": url, "short_part": short_part, "short_url": short_url,
                          "status": {"code": 2004,
                                     "message": "New short_part was generated successfully. "
                                                "Url, short_part and short_url was added to database successfully."}}
                print(result)
                with open("logs.log", "a", encoding="utf-8") as log_file:
                    log_file.write(str(result))

                return result

    # якщо url не відповідає патерну
    else:
        # якщо передається user_id i variation_sku_id
        if list(user_data.keys()).count("user_id") == 1 and list(user_data.keys()).count("variation_sku_id") == 1:

            result_error = {"url": url,
                            "user_id": user_data["user_id"],
                            "variation_sku_id": user_data["variation_sku_id"],
                            "status": {"code": 4001, "message": "Input correct url."}}
            print(result_error)
            with open("logs.log", "a", encoding="utf-8") as log_file:
                log_file.write(str(result_error))

            return result_error

        # якщо передається тільки user_id
        elif list(user_data.keys()).count("user_id") == 1 and list(user_data.keys()).count("variation_sku_id") == 0:

            result_error = {"url": url,
                            "user_id": user_data["user_id"],
                            "variation_sku_id": None,
                            "status": {"code": 4001, "message": "Input correct url."}}
            print(result_error)
            with open("logs.log", "a", encoding="utf-8") as log_file:
                log_file.write(str(result_error))

            return result_error

        # якщо передається тільки variation_sku_id
        elif list(user_data.keys()).count("user_id") == 0 and list(user_data.keys()).count("variation_sku_id") == 1:

            result_error = {"url": url,
                            "user_id": None,
                            "variation_sku_id": user_data["variation_sku_id"],
                            "status": {"code": 4001, "message": "Input correct url."}}
            print(result_error)
            with open("logs.log", "a", encoding="utf-8") as log_file:
                log_file.write(str(result_error))

            return result_error

        # якщо передається тільки url
        else:
            result_error = {"url": url,
                            "user_id": None,
                            "variation_sku_id": None,
                            "status":{"code": 4001, "message": "Input correct url."}}
            print(result_error)
            with open("logs.log", "a", encoding="utf-8") as log_file:
                log_file.write(str(result_error))

            return result_error


# API_2: Документація в файлі API_DOC.md
# Робота API через кеш
@app.route("/<short_part>")
@cache.cached(timeout=300)          # 5 minutes = 300 seconds
def find_main_url(short_part):

    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("logs.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"\n\n{current_datetime} Redirect to main_url from short_url (Cached process): \n")

    if short_part in sql.find_all_short_parts():

        # знаходимо в базі даних url по заданій short_part
        main_url = sql.find_url([short_part])

        # записуємо в базу +1 клік та дату кліка
        sql.update_redirect_clicks([short_part])

        result = {"short_part": short_part,
                  "url": main_url,
                  "status": {"code": 200,
                             "message": "Find main_url by short_part process was successful."
                                        "Short url will be redirected to main_url."}}
        print(result)
        with open("logs.log", "a", encoding="utf-8") as log_file:
            log_file.write(str(result))

        return redirect(main_url)

    else:
        result_error = {"short_part": short_part,
                        "status": {"code": 4004,
                                   "message": "Short part doesnt exist in database. Main_url cannot be founded."}}
        print(result_error)
        with open("logs.log", "a", encoding="utf-8") as log_file:
            log_file.write(str(result_error))

        return result_error


if __name__ == '__main__':
    app.run(debug=True)

    