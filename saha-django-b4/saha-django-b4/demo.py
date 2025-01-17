import psycopg2
import bcrypt

# Database connection settings
DB_SETTINGS = {
    'dbname': 'saha',
    'user': 'postgres',
    'password': 'Postgre@123',
    'host': 'localhost',
    'port': '5432'
}

def hash_and_update_passwords():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()

        # Query to fetch all users with plain-text passwords
        cursor.execute("SELECT id, password FROM \"User\"")  # Use correct table name and column
        users = cursor.fetchall()

        # Update each user's password to a bcrypt hash
        for user_id, plain_password in users:
            if plain_password:  # Ensure password field is not empty
                # Hash the plain-text password
                hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Update the password in the database
                update_query = "UPDATE \"User\" SET password = %s WHERE id = %s"
                print(f"Executing: {update_query}, Params: ({hashed_password}, {user_id})")
                cursor.execute(update_query, (hashed_password, user_id))

                # Confirm the update
                cursor.execute("SELECT password FROM \"User\" WHERE id = %s", (user_id,))
                updated_password = cursor.fetchone()[0]
                print(f"Updated password for user ID {user_id}: {updated_password}")

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        print("All passwords have been hashed and updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hash_and_update_passwords()
