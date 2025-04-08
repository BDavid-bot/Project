import sqlite3

def initialize_db(db_name, sql_file):
    try:
        conn = sqlite3.connect(db_name)
        print(f"Database '{db_name}' created and opened successfully.")

        with open(sql_file, 'r') as file:
            sql_script = file.read()
            conn.executescript(sql_script)
            print("Tables created successfully from create.sql")

        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    initialize_db("music_service.db", "create.sql")
