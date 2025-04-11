import sqlite3
import os
import json

def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json not found!")
        return {}

def execute_insert_sql(sql_file_path, db_path):
    if not os.path.exists(sql_file_path):
        print(f"The file '{sql_file_path}' does not exist!")
        return

    try:
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.executescript(sql_script)
        conn.commit()
        conn.close()

        print("insert.sql executed successfully.")

    except Exception as e:
        print(f"Error executing insert.sql: {e}")

if __name__ == "__main__":
    config = read_config()
    db_path = config.get("database_path", "music_service.db")
    sql_file_path = "insert.sql"

    execute_insert_sql(sql_file_path, db_path)
