from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/login', method=['POST'])
def login():
    id = request.formm.get('id')
    pw = request.formm.get('pw')
    print(f'입력한 ID는 {id}, PW는 {pw}')
    # if id == u['id'] and pw == u['pw']:

    return render_template('login.html', name = id)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['photo']
    print(file)
    return '파일 잘 받았음'

if __name__=='__main__':
    app.run(debug=True)