from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'hello1234'

items = [
    {'id': 'item1', 'name': '햄버거', 'price': 3000},
    {'id': 'item2', 'name': '핫도그', 'price': 2000},
    {'id': 'item3', 'name': '콜라', 'price': 1500},
]

users = [
    {'name': '홍길동', 'id': 'hong', 'pw': '1234'},
    {'name': '고길동', 'id': 'gil', 'pw': 'abcd'},
    {'name': '김길동', 'id': 'dong', 'pw': 'qwe123'},
]

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/remove_from_cart/<item_id>')
def remove_from_cart(item_id):

    cart = session.get('cart', {})

    if item_id in cart:
        del cart[item_id]

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('view_cart'))

@app.route('/')
def home():
    return render_template('home.html', user=session.get('user'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('view_cart'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None
    user = None

    if request.method == 'POST':

        id = request.form['id']
        pw = request.form['pw']

        print(f"입력값: {id}, {pw}")

        for u in users:
            if u['id'] == id and u['pw'] == pw:
                user = u
                break

        if user:
            session['user'] = user   # 🔥 이게 핵심
            return redirect(url_for('home'))  # 로그인 성공 후 이동
        else:
            error = "Invalid ID or PW"

    return render_template('login.html', user=session.get('user'), error=error)

@app.route('/products')
def products():
    return render_template('product.html', items=items)

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    # ✅ 로그인 체크 추가 (핵심)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    print("장바구니에 담을 상품: ", item_id)
    if 'cart' not in session:
        session['cart'] = {}

    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        # 장바구니에 담을 상품이 실제로 존재하는가??
        session['cart'][item_id] = 1

    print(session['cart'])
    session.modified = True  # 세션 데이터가 수정되었음을 flask에게 인지시킴

    return redirect(url_for('products'))

@app.route('/cart')
def view_cart():
     # ✅ 로그인 체크 추가
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = {}
    total_price = 0

    for item_id, quantity in session.get('cart', {}).items():
        item = next((i for i in items if i['id'] == item_id), None)
        cart_items[item_id] = {
            'name': item['name'],
            'quantity': quantity,
            'price': item['price']
        }
        total_price += item['price'] * quantity

    return render_template('cart.html', cart_items=cart_items, total_price=total_price) # 여기에 장바구니에 담긴 상품 채워넣기

if __name__ == '__main__':
    app.run(debug=True)
