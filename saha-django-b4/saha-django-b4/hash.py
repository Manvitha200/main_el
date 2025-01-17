import psycopg2
import bcrypt

# Database connection settings
DB_SETTINGS = {
    'dbname': 'saha',        # Your database name
    'user': 'postgres',      # Your PostgreSQL username
    'password': 'Postgre@123',  # Your PostgreSQL password
    'host': 'localhost',     # Database host
    'port': '5432'           # Database port
}

def hash_and_update_passwords():
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        
        # Query to fetch all users with plain-text passwords
        cursor.execute("SELECT user_id, password_hashed FROM \"User\"")  # Adjusted for your table and column names
        users = cursor.fetchall()
        
        # Update each user's password to a bcrypt hash
        for user_id, plain_password in users:
            if plain_password:  # Ensure password_hashed field is not empty
                # Hash the plain-text password
                hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Update the password in the database
                cursor.execute(
                    "UPDATE \"User\" SET password_hashed = %s WHERE user_id = %s",
                    (hashed_password, user_id)
                )
                print(f"Updated password for user ID {user_id}")

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        print("All passwords have been hashed and updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hash_and_update_passwords()
