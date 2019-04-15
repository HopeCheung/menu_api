import os
import sqlite3

conn = sqlite3.connect("menu.db")

#conn.execute('create table menu (id int, name varchar(20))')
cur = conn.cursor()

#cur.execute('insert into menu values(1, "Lunch Specials")')
#cur.execute('insert into menu values(2, "Dinner Specials")')
cur.execute('insert into menu values(3, "Specials of the day")')
conn.commit()

cur = conn.cursor()
cur.execute("select * from menu")
print(cur.fetchall())
