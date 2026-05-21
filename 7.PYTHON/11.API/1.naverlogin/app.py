from flask import Flask, render_template, redirect, request, session, url_for
from dotenv import load_dotenv
import requests
import os

load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')
callback_uri = os.getenv('NAVER_REDIRECT_URI')

app = Flask(__name__)
app.secret_key = os.getenv('MY_SESSION_KEY')

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/api/naver/callback')
def naver_callback():
    code = request.args.get('code')
    state = request.args.get('state') # 내가 준 값이 맞는지 봐야함, 현재는 연습이기에 생략 예정

    # 위 코드를 가지고 네이버에게 확인 요청함
    token_url = (
        f'https://nid.naver.com/oauth2.0/token?'
        f'grant_type=authorization_code&client_id={client_id}'
        f'&redirect_uri={callback_uri}&state=HELLO'
    )

    token_response = requests.get(token_url).json()
    access_token = token_response.get('access_token')
    print(access_token)

    # 나와 사용자에 대한 검증이 끝나고 네이버와 대화할 수 있는 인증 토큰(access_token)을 받아와서 이걸로 사용자의 정보를 물어본다.
    profile_url = {
        f'{https://openai.naver.com/v1/nid/me}'
    }
    headers = {'Authorization': f'Bearer {access_token}'}

    profile = requests.get(profile_url, headers=headers).json()
    print('서버측 사용자 정보 응답: ', profile)
    # 필수 동의항목은 다 받아오고 선택 동의항목은 사용자가 동의하고 가입했다면 받아올 수 있음. 동의하지 않았다면 받아올 수 없음.
    session['user'] = profile['response']

    return "인증은 일단 성공, 당신이 누구인지는 모름."

@app.route('/login')
def naver_login():

    auth_url = (
        f'https://nid.naver.com/oauth2.0/authorize?'
        f'response_type=code&client_id={client_id}'
        f'&redirect_uri={callback_uri}&state=HELLO'
    )

    print(auth_url)
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)