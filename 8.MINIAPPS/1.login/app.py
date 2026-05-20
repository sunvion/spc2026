from flask import Flask, render_template, request
from flask import session, flash, redirect, url_for
from datetime import timedelta

import sqlite3

app = Flask(__name__)
app.secret_key = 'hello1234' # 실무적으로는 이런 민감한 credential을 커밋하지 않음.
app.permanent_session_lifetime = timedelta(minutes = 5)

DATABASE = 'users.sqlite3' # 나의 파일명

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # 나의 결과를 다 Dict 포맷으로 관리
                                   # row[0] => row['id'] 이런식으로 접근 가능
    return conn

def init_db():
    with app.app_context(): # flask app 초기화 완료된 후
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL)
            ''')
        
        # 기본 계정 추가
        cur.execute('SELECT COUNT(*) AS count FROM users')
        count = cur.fetchone()['count']
        if count == 0:
            cur.execute('INSERT INTO users (username, password) VALUES (?,?)', ("user1", "password1")) # 실무적으로는 암호화된 비밀번호가 들어감.
            cur.execute('INSERT INTO users (username, password) VALUES (?,?)', ("user2", "password2"))
        conn.commit()

        # 부팅시 계정 정보 출력
        cur.execute('SELECT * FROM users')
        rows = cur.fetchall()

        print('-' * 30)

        for row in rows:
            print(f"id       : {row['id']}")
            print(f"username : {row['username']}")
            print(f"password : {row['password']}")
            print('-' * 30)

        conn.close()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user_data = cur.fetchone()
        conn.close()

        if user_data:
            session['user'] = username
            flash('로그인에 성공하였습니다.')
            return redirect(url_for('home'))
        else:
            flash('로그인에 실패하였습니다.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    flash('성공적으로 로그아웃이 되었습니다.')
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__" :
    init_db()
    app.run(debug=True) # 실무적으로는 디버그는 꼭 끌 것