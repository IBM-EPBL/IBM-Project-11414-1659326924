import sqlite3
conn = sqlite3.connect("datab.sqlite")
cursor = conn.cursor()
quer = """CREATE TABLE User (
      id integer primary key
      email text NOT NULL,
      username text NOT NULL,
      rollnumber integer PRIMARY KEY,
      password text NOT NULL
)"""
cursor.execute(quer)