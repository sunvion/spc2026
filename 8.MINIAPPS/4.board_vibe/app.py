import os
import sqlite3
from flask import Flask, request, jsonify, render_template, g

app = Flask(__name__)
DATABASE = 'board.db'

# 데이터베이스 연결 가져오기
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # 딕셔너리 형태로 결과를 반환받기 위해 row_factory 설정
        db.row_factory = sqlite3.Row
    return db

# 데이터베이스 연결 닫기
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 데이터베이스 및 테이블 초기화
def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            db.commit()
            print("SQLite Database & 'posts' table initialized successfully.")

# 1. 메인 화면 렌더링 라우트
@app.route('/')
def index():
    return render_template('index.html')

# 2. API: 전체 게시글 목록 최신순 조회
@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, title, message, created_at FROM posts ORDER BY id DESC")
        rows = cursor.fetchall()
        
        posts = []
        for row in rows:
            posts.append({
                'id': row['id'],
                'title': row['title'],
                'message': row['message'],
                'created_at': row['created_at']
            })
            
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. API: 신규 게시글 추가
@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '유효하지 않은 요청 데이터입니다.'}), 400
            
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        
        # 유효성 검사
        if not title:
            return jsonify({'error': '제목을 입력해주세요.'}), 400
        if not message:
            return jsonify({'error': '내용을 입력해주세요.'}), 400
            
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO posts (title, message) VALUES (?, ?)",
            (title, message)
        )
        db.commit()
        
        # 삽입된 데이터 가져오기
        post_id = cursor.lastrowid
        cursor.execute("SELECT id, title, message, created_at FROM posts WHERE id = ?", (post_id,))
        new_row = cursor.fetchone()
        
        new_post = {
            'id': new_row['id'],
            'title': new_row['title'],
            'message': new_row['message'],
            'created_at': new_row['created_at']
        }
        
        return jsonify(new_post), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. API: 특정 게시글 삭제
@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 존재 여부 확인
        cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not cursor.fetchone():
            return jsonify({'error': '해당 게시글이 존재하지 않습니다.'}), 404
            
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        db.commit()
        
        return jsonify({'success': True, 'message': '게시글이 성공적으로 삭제되었습니다.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 5. API: 특정 게시글 수정
@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': '유효하지 않은 요청 데이터입니다.'}), 400
            
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        
        # 유효성 검사
        if not title:
            return jsonify({'error': '제목을 입력해주세요.'}), 400
        if not message:
            return jsonify({'error': '내용을 입력해주세요.'}), 400
            
        db = get_db()
        cursor = db.cursor()
        
        # 존재 여부 확인
        cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not cursor.fetchone():
            return jsonify({'error': '해당 게시글이 존재하지 않습니다.'}), 404
            
        # 데이터 업데이트
        cursor.execute(
            "UPDATE posts SET title = ?, message = ? WHERE id = ?",
            (title, message, post_id)
        )
        db.commit()
        
        # 업데이트된 최신 데이터 가져오기
        cursor.execute("SELECT id, title, message, created_at FROM posts WHERE id = ?", (post_id,))
        updated_row = cursor.fetchone()
        
        updated_post = {
            'id': updated_row['id'],
            'title': updated_row['title'],
            'message': updated_row['message'],
            'created_at': updated_row['created_at']
        }
        
        return jsonify(updated_post), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 앱 실행 전에 DB 및 테이블 초기화 진행
    init_db()
    app.run(debug=True, port=5000)
