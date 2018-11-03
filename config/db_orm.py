import sqlite3
from .meta import DATABASE_PATH

def connect_to_database(func):

    def wrapper_func(*args, **kwargs):

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        output = func(*args, cursor, **kwargs)

        if kwargs.get('commit') == True:
            connection.commit()

        connection.close()

        return output

    return wrapper_func
