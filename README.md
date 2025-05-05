
# URL Shortener Service API

This is a Flask-based API Service for shortening URLs with optional user_id and variation_sku_id parameters. 
It is built with Python (Flask) and uses a SQL-based database to store all links and short URLs.
It supports short URL generation, redirection, caching, and logging of user actions and requests.
This URL Shortener Service API is used in my chatbot "Pricer_bot".

## Features

- Generate short URLs for long links.
- Associate short URLs with user_id and variation_sku_id.
- Avoids duplicate entries for the same user/sku combination.
- Redirection from short URL to original link with caching.
- Logging of all operations and API responses.
- Environment configuration using .env.

## Technologies Used

- Python 3.8+
- Flask
- Flask-Caching
- dotenv
- SQLite or any other SQL-based database
- Regex
- Logging
- REST API