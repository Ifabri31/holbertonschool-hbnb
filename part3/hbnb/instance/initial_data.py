import bcrypt
import uuid
import sqlite3


sqliteConnection = sqlite3.connect('development.db')
c = sqliteConnection.cursor()

password = 'admin1234'
password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

user_id = str(uuid.uuid4())

user_table = """
INSERT INTO users(id, first_name, last_name, email, password, is_admin)
VALUES (?, ?, ?, ?, ?, ?);
"""

user_data = (user_id, 'Admin', 'HBnB', 'admin@hbnb.io', password_hashed, True)

amenity_table = """
INSERT INTO amenities(id, name) 
VALUES (?, ?)
"""

amenity_data = [
    (str(uuid.uuid4()), 'Wifi'),
    (str(uuid.uuid4()), 'Swimming Pool'),
    (str(uuid.uuid4()), 'Air Conditioning')
]

c.execute(user_table, user_data)
c.executemany(amenity_table, amenity_data)


sqliteConnection.commit()

c.close()
sqliteConnection.close()