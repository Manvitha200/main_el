# import psycopg
# from config import config

# def connect():
#     connection=None
#     params=config()
#     print('Connecting to the PostgreSQL DB..')
#     connection=psycopg.connect(**params)

#     #creating cursor
#     crsr=connection.cursor()

#     if connection is not None:
#         connection.close()
#         print('Sessopm terminated')

# if __name__=="__main__":
#     connect()

# # import psycopg

# # try:
# #     connection = psycopg.connect(
# #         dbname="saha",
# #         user="postgres",
# #         password="212921",
# #         host="localhost",
# #         port="5432"
# #     )
# #     print("Connection successful!")
# #     connection.close()
# # except Exception as error:
# #     print(f"Error connecting to the database: {error}")








import psycopg
import os

def config():
    """
    Returns a dictionary of database connection parameters.
    Sensitive information is fetched from environment variables for security.
    """
    return {
        "dbname": os.getenv("DB_NAME", "saha"),  # Default to 'saha' if not set
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "Postgre@123"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
    }

def connect():
    """
    Connects to the PostgreSQL database using parameters from the `config` function.
    Executes a simple query to test the connection and closes the connection gracefully.
    """
    connection = None
    try:
        params = config()
        print("Connecting to the PostgreSQL database...")
        
        # Establish connection
        connection = psycopg.connect(**params)
        print("Connection successful!")

        # Creating cursor and executing a test query
        crsr = connection.cursor()
        crsr.execute("SELECT version();")
        db_version = crsr.fetchone()
        print(f"PostgreSQL version: {db_version[0]}")

    except Exception as error:
        print(f"Error connecting to the database: {error}")
    finally:
        # Ensure the connection is closed
        if connection is not None:
            connection.close()
            print("Session terminated.")


if __name__ == "__main__":
    connect()
