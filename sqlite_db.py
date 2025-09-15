import sqlite3 as sqlite
import json

class Database:
    def __init__(self, path = ":memory:"):
        self.path = path

    def __enter__(self):
        self.con = sqlite.connect(self.path)
        self.cur = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.con.commit()
        self.con.close()

    def query(self, query: str, params: tuple = ()):
        res = self.cur.execute(query, params)
        return res.fetchall()

    def execute(self, statement: str, params: tuple = ()):
        self.cur.execute(statement, params)
        self.con.commit()
    
    def execute_many(self, statement: str, params: list[tuple] = []):
        self.cur.executemany(statement, params)
        self.con.commit()


if __name__ == "__main__":
    with Database() as db:
        db.execute("CREATE TABLE mytable(id, name, type);")
        db.execute_many("INSERT INTO mytable VALUES(?, ?, ?)", [(1, "item1", "TYPE_1"), (2, "item2", "TYPE_2")])
        rows = db.query("SELECT * FROM mytable;")
        print(f"{json.dumps(rows, indent=2)}")