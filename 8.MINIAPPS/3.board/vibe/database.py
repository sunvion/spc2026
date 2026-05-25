import sqlite3


class MyDatabase():
    def __init__(self):
        self.db = sqlite3.connect(
            'board.sqlite',
            check_same_thread=False
        )

        self.db.row_factory = sqlite3.Row

        self.cursor = self.db.cursor()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def execute_fetch(self, query, args={}):
        self.cursor.execute(query, args)
        result = self.cursor.fetchall()
        return result

    def commit(self):
        self.db.commit()


if __name__ == "__main__":
    print('여기는 DB 테스트')

    db = MyDatabase()

    db.execute('''
    CREATE TABLE IF NOT EXISTS board (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(50),
        message VARCHAR(200)
    )
    ''')

    db.commit()

    result = db.execute_fetch("SELECT * FROM board")

    for r in result:
        print(r['id'], r['title'], r['message'])