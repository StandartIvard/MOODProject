import sqlite3


def getInformDB(name):
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    return cur.execute("SELECT * FROM users WHERE username = '" + name + "'").fetchall()


def insertUserDB(name, password):
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES('" + name + "','" + password + "', 0)")
    con.commit()
