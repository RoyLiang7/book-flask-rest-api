"""
#
# ---- https://www.pythonmorsels.com/making-singletons/#:~:text=Python's%20modules%20act%20like%20singletons,need%20a%20class%20in%20Python.&text=For%20each%20Python%20module%2C%20there,global%20variables%20within%20a%20module.
#
"""

import os
import mysql.connector

config = {
  'user'             : os.environ["MYSQL_USER"],
  'password'         : os.environ["MYSQL_PASSWORD"],
  'host'             : os.environ["MYSQL_HOST"],
  'database'         : os.environ["MYSQL_DB"],
  'raise_on_warnings': True
}

# --- connection
# cnx = mysql.connector.connect(**config)

# ---- pooling
# -- https://dev.mysql.com/doc/connector-python/en/connector-python-connection-pooling.
# -- https://medium.com/@pardeep.singh14/setting-up-a-flask-application-with-connection-pooling-dfce896a0841
pool = mysql.connector.pooling.MySQLConnectionPool(
          pool_name="mypool", 
          pool_size=5,
          **config
)
cnx = pool.get_connection()
