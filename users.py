import json
import os
from datetime import datetime

# Function to read the config and load users data from the JSON file
def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  config.json not found!")
        return {}

# Function to load users from the JSON file (creates the file if it doesn't exist)
def load_users():
    config = read_config()
    users_path = config.get("users_path", "users.json")

    # If the file doesn't exist, create it with an empty list
    if not os.path.exists(users_path):
        with open(users_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        print(f"⚠️ {users_path} was missing, so a new empty file was created.")
        return []

    with open(users_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Function to save users data back into the JSON file
def save_users(users):
    config = read_config()
    users_path = config.get("users_path", "users.json")

    with open(users_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

# Function to generate SQL for users (insert into insert.sql)
def generate_user_insert_sql(users):
    lines = []

    # Inserting into Users Table
    lines.append("\n-- Inserting into Users Table")
    for user in users:
        lines.append(
            f"INSERT INTO Users (UserID, Username, Email, JoinDate) VALUES "
            f"({user['UserID']}, '{user['Username'].replace("'", "''")}', "
            f"'{user['Email'].replace("'", "''")}', '{user['JoinDate']}');"
        )

    return "\n".join(lines)

# Example usage:
if __name__ == "__main__":
    # Generating SQL to insert into the database
    users_sql = generate_user_insert_sql(load_users())

    # Append the generated SQL to insert.sql
    with open("insert.sql", "a", encoding="utf-8") as f:
        f.write(users_sql)

    print("SQL for users table has been added to insert.sql.")
