import sqlite3

conn = sqlite3.connect('example.db')
cur = conn.cursor()

cur.execute("SELECT*FROM users")

# 커서가 실행한 결과 받기
rows = cur.fetchall()
print(rows)

conn.close()