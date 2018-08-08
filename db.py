import sqlite3
import pandas as pd

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("items.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS item (id INTEGER PRIMARY KEY, name TEXT, idate TIMESTAMP DEFAULT CURRENT_TIMESTAMP, upc TEXT, quantity INTEGER)")
        self.conn.commit()

    def insert(self, name, upc):
        self.cur.execute("INSERT INTO item VALUES (null,?,CURRENT_TIMESTAMP,?,1)",(name,upc))
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM item")
        rows = self.cur.fetchall()
        return rows

    def pandasview(self):
        conn = sqlite3.connect("items.db")
        view = pd.read_sql_query("SELECT * FROM item",conn)
        return view

    def delete(self,id):
        self.cur.execute("DELETE FROM item WHERE id=?",(id,))
        self.conn.commit()

    def selectbyid(self, quantity, id):
        self.cur.execute("UPDATE item SET quantity = ? WHERE id =?",(quantity,id))
        self.conn.commit()

    def update(self, name, idate, upc, expiration):
        self.cur.execute("UPDATE item SET name =?, idate=?, upc=?, expiration =? WHERE name=?",(name,idate,upc,expiration))
        self.conn.commit()

    def checkforitem(self,upc):
        self.cur.execute("SELECT upc FROM item where upc=?",(upc,))
        rows = self.cur.fetchall()
        return rows

    def findnamebyupc(self,upc):
        self.cur.execute("SELECT name FROM item WHERE upc =?",(upc,))
        names = self.cur.fetchall()
        return names

    def selectbyupc(self, upc):
        self.cur.execute("UPDATE item SET quantity = quantity + 1 WHERE upc = ?",(upc,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
