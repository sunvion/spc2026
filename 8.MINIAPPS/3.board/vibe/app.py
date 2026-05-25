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


# 게시글 작성
@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()

    title = data.get('title')
    message = data.get('message')

    sql = "INSERT INTO board (title, message) VALUES (?, ?)"
    db.execute(sql, (title, message))
    db.commit()

    return jsonify({'result': 'success'})


# 게시글 목록 조회
@app.route('/list')
def list():
    sql = "SELECT * FROM board"

    result = db.execute_fetch(sql)

    dict_list = [
        {
            'id': r['id'],
            'title': r['title'],
            'message': r['message']
        }
        for r in result
    ]

    return jsonify({
        'result': 'success',
        'data': dict_list
    })


# 게시글 삭제
@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()

    board_id = data.get('id')

    sql = "DELETE FROM board WHERE id=?"
    db.execute(sql, (board_id,))
    db.commit()

    return jsonify({'result': 'success'})


# 게시글 수정
@app.route('/modify', methods=['POST'])
def modify():
    data = request.get_json()

    board_id = data.get('id')
    title = data.get('title')
    message = data.get('message')

    sql = """
    UPDATE board
    SET title=?, message=?
    WHERE id=?
    """

    db.execute(sql, (title, message, board_id))
    db.commit()

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run(debug=True)