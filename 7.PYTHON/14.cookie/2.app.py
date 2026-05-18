from flask import Flask, make_response, request

app = Flask(__name__)

@app.route("/")
def set_cookie():
    resp = make_response("Cookie has been set!!")
    resp.set_cookie("my-data", "spc2026")
    return resp

@app.route("/user")
def get_cookie():
    cookie = request.cookies.get('my-data')
    print(cookie)

    return f"안녕, {cookie} 야"

if __name__ == "__main__":
    app.run(debug=True)
