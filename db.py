import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    Returns a connection object or a string with the error message.
    """
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        return conn
    except Exception as e:
        return str(e)
