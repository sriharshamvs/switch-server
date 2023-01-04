import csv
import sqlite3


def create_topics():
    print("Creating table: Topics")
    con = sqlite3.connect("smartHome.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE topics (room, device, topic, status, icon, location);")

    with open('db_csv/topics.csv','r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['room'], i['device'], i['topic'], i['status'], i['icon'], i['location']) for i in dr]

    cur.executemany("INSERT INTO topics (room, device, topic, status, icon, location) VALUES (?, ?, ?, ?, ?, ?);", to_db)
    con.commit()
    con.close()


def create_users():
    print("Creating table: Users")
    con = sqlite3.connect("smartHome.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE users (username, password, room);")

    with open('db_csv/users.csv','r') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['username'], i['password'], i['room']) for i in dr]

    cur.executemany("INSERT INTO users (username, password, room) VALUES (?, ?, ?);", to_db)
    con.commit()
    con.close()


if __name__ == "__main__":

    create_topics()
    create_users()