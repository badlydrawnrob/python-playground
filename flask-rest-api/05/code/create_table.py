import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# Normally, you could use `int` or `INTEGER`
# - When creating auto-incrementing primary key
#   you MUST use `INTEGER`
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# `real` is just a number with a decimal point
create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()