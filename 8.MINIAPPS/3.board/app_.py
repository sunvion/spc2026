from flask import Flask
from flask import send_from_directory
from flask import request
from flask import jsonify

from database import MyDatabase

app = Flask(__name__)
db = MyDatabase()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/create', methods=['POST'])
def create():

    # 1. 데이터 받기
    title = request.form.get('title')
    message = request.form.get('message')

    # 2. SQL 작성
    sql = """
    INSERT INTO board (title, message)
    VALUES (?, ?)
    """

    # 3. DB 실행
    db.execute(sql, (title, message))

    # 4. 결과 반환
    return jsonify({'result': 'success'})

@app.route('/list')
def list():

    sql = "INSERT INTO board (title, message)"

    rows = db.fetchall(sql)

    return jsonify(rows)

@app.route('/delete', methods=['POST'])
def delete():

    post_id = request.form.get('id')

    sql = "DELETE FROM board WHERE ________"

    db.execute(sql, (_________))

    return jsonify({'result':'success'})

@app.route('/modify', methods=['POST'])
def modify():

    post_id = request.form.get('id')
    title = request.form.get('title')
    message = request.form.get('message')

    sql = """
    UPDATE board
    SET __________
    WHERE ________
    """

    db.execute(sql, (________________))

    return jsonify({'result':'success'})


if __name__ == '__main__':
    app.run(debug=True)
