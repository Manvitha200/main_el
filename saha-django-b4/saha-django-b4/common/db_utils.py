import psycopg2
from psycopg2.extras import RealDictCursor

DB_SETTINGS = {
    'dbname': 'saha',
    'user': 'postgres',
    'password': 'Postgre@123',  # Replace with your credentials
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
