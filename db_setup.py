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

# def insert_data(db_name, sql_file):
#     try:
#         conn = sqlite3.connect(db_name)
#         with open(sql_file, 'r') as file:
#             sql_script = file.read()
#             conn.executescript(sql_script)
#             print("Data inserted successfully from insert.sql")
#         conn.close()
#     except Exception as e:
#         print(f"An error occurred during insertion: {e}")

# def perform_crud(db_name, sql_file):
#     try:
#         conn = sqlite3.connect(db_name)
#         with open(sql_file, 'r') as file:
#             sql_script = file.read()
#             conn.executescript(sql_script)
#             print("CRUD operations performed successfully from crud.sql")
#         conn.close()
#     except Exception as e:
#         print(f"An error occurred during CRUD operations: {e}")

if __name__ == "__main__":
    initialize_db("music_service.db", "create.sql")
    insert_data("music_service.db", "insert.sql")
    perform_crud("music_service.db", "crud.sql")
