"""
#
# ---- https://www.doppler.com/blog/environment-variables-in-python
# ---- https://realpython.com/python-modules-packages/#reloading-a-module
# ---- https://www.doppler.com/blog/environment-variables-in-python
# ---- https://arjancodes.com/blog/organizing-python-code-with-packages-and-modules/
#
"""


import os
from flask import Flask


# ======================== f l a s k   a p p ======================= #
app = Flask(__name__)




# =============== c o n f i g u r a t i o n   f i l e =============== #
import configparser
from datetime import timedelta

config = configparser.ConfigParser()
config.read('./src/config.ini')     ### have to declare path from root folder



# ============ e n v i r o n m e n t   v a r i a b l e s ============ #
# ---- https://medium.com/@dataproducts/python-three-different-ways-to-store-environment-variables-15224952f31b
# ---- https://developer.vonage.com/en/blog/python-environment-variables-a-primer

os.environ["MYSQL_HOST"]     = config['MYSQL']['HOST']
os.environ["MYSQL_USER"]     = config['MYSQL']['USER']
os.environ["MYSQL_PASSWORD"] = config['MYSQL']['PWD']
os.environ["MYSQL_DB"]       = config['MYSQL']['DB']

# *** OR *** for sqlalchemy
os.environ["MYSQL_CONNECTOR"] = "mysql+mysqlconnector://{user}:{password}@{host}[:{port}]/{dbname}".format(
    user     = config['MYSQL']['USER'],
    password = config['MYSQL']['PWD'],
    host     = config['MYSQL']['HOST'],
    port     = config['MYSQL']['PORT'],
    dbname   = config['MYSQL']['DB']
)


# =========== a p p l i c a t i o n   v a r i a b l e s ============== #
# --- configurations for *flask jwt extended library
app.config["JWT_SECRET_KEY"] = config['JWT']['SECRET_KEY']
app.config['JWT_TOKEN_LOCATION'] = 'headers'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=5)

# --- configurations for *flask-basicauth module
app.config['BASIC_AUTH_USERNAME'] = config['BASIC_AUTH']['USERNAME']
app.config['BASIC_AUTH_PASSWORD'] = config['BASIC_AUTH']['PASSWORD']
# app.config["BASIC_AUTH_REALM"] = "Login Required"



# ========================= r o u t i n g ============================= #
# ---- https://realpython.com/flask-blueprint/

from src.controllers.user_controller           import user_bp
from src.controllers.role_controller           import role_bp
from src.controllers.book_trans_controller     import trans_bp
from src.controllers.book_category_controller  import cat_bp
from src.controllers.book_type_controller      import type_bp

app.register_blueprint(user_bp,  url_prefix="/book/user")
app.register_blueprint(role_bp,  url_prefix="/book/role")
app.register_blueprint(type_bp,  url_prefix="/book/type")
app.register_blueprint(cat_bp,   url_prefix="/book/category")

app.register_blueprint(trans_bp, url_prefix="/book/transaction")

# ========================= l o g g i n g ============================== #
# ---- https://docs.python.org/3/library/logging.handlers.html
# ---- https://docs.python-guide.org/writing/logging/
# ---- https://www.loggly.com/ultimate-guide/python-logging-basics/

import logging
import logging.handlers

# --- set file handler for writes to an external file
handler = logging.handlers.WatchedFileHandler("./logs/error.log")
# --- logging format
log_format_1 = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s- %(message)s")
log_format_2 = logging.BASIC_FORMAT
handler.setFormatter(logging.Formatter(log_format_2))
# 
logger = logging.getLogger(__name__)
logger.addHandler(handler)



# ==================== e r r o r   h a n d l i n g ===================== #
# --- https://flask.palletsprojects.com/en/stable/errorhandling/
from flask import jsonify
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception(f"{str(e)}")

    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return jsonify("HTTP Exception !!!"), 500    # -- should just return a generic message, details are in the log file
        # return jsonify(error=str(e)), 500
    else:
        return jsonify("NORMAL Exception !!!"), 500  # -- should just return a generic message, details are in the log file
        # return jsonify(error=str(e)), 500
