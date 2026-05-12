from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {'name': 'Alice', 'age': 25, 'phone': '123-456-7890'},
    {'name': 'Bob', 'age': 30, 'phone': '123-555-7890'},
    {'name': 'Charlie', 'age': 27, 'phone': '123-777-7890'}
]
# 파이썬의 리스트 폼, 각각의 리스트에는 딕셔너리

@app.route('/')
def main():
    return jsonify(users) # 백엔드 list/dict 구조를 웹이 좋아하는 JSON 포멧으로 만듬

@app.route('/user/<name>')
def get_user_by_name(name):
    print('사용자입력값: ', name)
    user = None
    for u in  users:
        if u['name'].lower() == name.lower():
            user=u

    if user:
        return jsonify(user)
    else :
        return jsonify({'message': "사용자를 찾지 못했습니다."})
    
if __name__ == '__main__':
    app.run(debug=True)