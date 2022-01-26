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


def updatePassword(name, password):
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET password = '" + password + "' WHERE username = '" + name + "';")
    con.commit()


def updateHP(name, HP):
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET HP = " + str(HP) + " WHERE username = '" + name + "';")
    con.commit()


def updateScore(name, score):
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET score = " + str(score) + " WHERE username = '" + name + "';")
    con.commit()


def updateTime(name, time):
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    cur.execute("UPDATE users SET btime = " + str(time) + " WHERE username = '" + name + "';")
    con.commit()


def getTime():
    con = sqlite3.connect('data/usersDB.db')
    cur = con.cursor()
    cur.execute("SELECT name, score, btime FROM users")