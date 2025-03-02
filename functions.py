import sqlite3

def create_table():
    conn = sqlite3.connect('database.db')
    query = "CREATE TABLE Data(Username text, Multiplier Real, Score Real, Image BLOB)"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()

def select_data(required_columns):
    conn = sqlite3.connect('database.db')
    query = "SELECT {} FROM Users".format(', '.join(required_columns))
    cursor = conn.cursor()
    cursor.execute(query)
    recieved_data = cursor.fetchall()
    return recieved_data

def insert_data(data):
    conn = sqlite3.connect("database.db")
    query = "INSERT INTO Users(Username, Password) VALUES(?,?)"
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()

def specific_user_credentials(username):
    conn = sqlite3.connect("database.db")
    query = "SELECT * FROM USERS WHERE Username == ?"
    cursor = conn.cursor()
    cursor.execute(query, (username,))
    credentials = cursor.fetchone()
    return credentials

def increase_multiplier(username):

    conn = sqlite3.connect("database.db")
    query = "UPDATE Data Set multiplier = multiplier + 0.1 Where Username == ?"

    cursor = conn.cursor()
    cursor.execute(query, (username,))
    conn.commit()

def calculate_score(username):
    conn = sqlite3.connect("database.db")
    query = "UPDATE Data SET Score = Score + 100*Multiplier Where username == ?"
    cursor = conn.cursor()
    cursor.execute(query, (username,))
    conn.commit()


def insert_art_into_data(username, art):

    increase_multiplier(username)
    calculate_score(username)

    file = open(art, 'rb')
    image_blob = file.read()

    conn = sqlite3.connect("database.db")
    query = "UPDATE Data SET Image = ? Where Username = ?"

    cursor = conn.cursor()
    cursor.execute(query, (image_blob, username))
    conn.commit()

def get_art_from_username(username):


    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT Image FROM Data Where Username == ?"
    cursor.execute(query, (username, ))
    images = cursor.fetchall()
    return images

def assign_mult_and_score_to_user(username):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "INSERT INTO Data(username, multiplier, score, image) VALUES(?,?,?,?)"
    cursor.execute(query, (username,1,0,'0'))
    conn.commit()

def sql_queries():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("delete from users")
    conn.commit()


def fetch_score(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT Score from Data where username==?"
    cursor.execute(query, (username,))
    score = cursor.fetchone()
    return score





