import sqlite3

# Connect to database file
connection = sqlite3.connect('data.db')
# Allows positioning of cursor to edit file
cursor = connection.cursor()
# Defines a schema
create_table = "CREATE TABLE users (id int, username text, password text)"
# Run the query
cursor.execute(create_table)


##
# Create a user
##

user = (1, 'jose', 'asdf')
# Insert the user query
# - You can use question marks as placeholder
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# Now actually add the user
cursor.execute(insert_query, user)


##
# Create lots of users
##

users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')
]
cursor.executemany(insert_query, users)


##
# Find users
##

select_query = "SELECT * FROM users"
# iterate as if command is a list
for row in cursor.execute(select_query):
    print(row)

##
# Save database and close
##

connection.commit()
connection.close()
