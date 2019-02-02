"""
app_dal module is used as a data access layer.

Author: Srinivas Rao Cheeti
email: srinivascheeti1@gmail.com
Date: Feb 2, 2019
"""
import mysql.connector

try:
    import logging
except Exception as e:
    print(e)


class AppDAL:
    def __init__(self, level):
        self.logs = logging.basicConfig(level=level)

    def get_sql_connection(self):
        """Establishes a connection to MySQL database

        :return: Returns a connection to mysql.
        """
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'dockerdb'
        }
        try:
            connection = mysql.connector.connect(**config)
            return connection
        except Exception as e:
            self.logs.error(e)
            raise e
