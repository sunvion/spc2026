from flask import Flask, render_template, request
from flask import session, redirect, url_for

# Session은 더이상 안함 -> 나중엔 이게 DB 에서 대체함

app = Flask(__name__)
app.secret_key = 'my-random-key'

# 사용자 DB
users = [
    {'name':'Alice', 'id':'alice', 'pw':'alice'},
    {'name':'Bob', 'id':'bob', 'pw':'bob1234'},
    {'name':'Charlie', 'id':'charlie', 'pw':'hello'},
]

@app.route('/dashboard')
def welcome():
    user = session.get('user')
    return render_template('dashboard.html', name=user['name'])

@app.route('/', methods=['GET'])
def home():
    if session.get('user'):
        return redirect(url_for('welcome'))
    # 로그인한 적이 없을 때, 그냥 첫 방문
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST' :
        # 1. 요청에서 id/pw 가져온다
        # id = 입력한 아이디, pw = 입력한 pw
        id = request.form.get('id')
        pw = request.form.get('pw')

        # 2. user db에서 이 사용자 매칭한다.
        user = next((u for u in users if u['id'] == id and u['pw'] == pw), None)

        # 3. 사용자가 있으면?
        if user:
            session['user'] = user # 로그인한 사용자를 세션에 저장한다.
            error = None
            return redirect(url_for('welcome'))
        else:
            error = "Invalid ID of password"

        return render_template('index.html', error=error)
    
    # 로그인이 아닐 때, 그냥 첫 방문
    return render_template('Index.html', error=error)

# 1. 사용자가 비밀번호를 바꾸는 기능을 추가한다.
# 1-1. method를 POST로 확장
# 1-2. users 안에서 나의 비번을 바꾼다.
# 1-3. 성공적으로 변경되면 나의 profile에서 확인한다.
# 1-4. '비밀번호 변경'을 눌렀을 때 성공적으로 변경되었음을 알려준다. (사용자 피드백)

@app.route('/profile', methods=['GET','POST'])
def profile():
    user = session.get('user')
    if not user:
        return redirect(url_for('home')) # 로그인 되지 않았다면 강제로 페이지 이동
    
    if request.method == 'POST':
        new_pw = request.form.get('new_pw')
        for u in users:
            if u['id'] == user['id']:
                u['pw'] = new_pw
                user['pw'] = new_pw
                session['user'] = user   # ⭐ 중요, 세션이 자동 갱신되게 만들어줌. (구 -> 신 버전으로 갱신)
                
                message = '성공적으로 비밀번호가 변경되었습니다.'
                # return render_template('profile.html', user=user, message=message)
                return render_template(url_for('profile'))

    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None) # 키가 없을 때, 즉 로그아웃 두번 했을 때 오류 방지됨.
    return redirect(url_for('home'))

if __name__ == '__main__' :
    app.run(debug=True)