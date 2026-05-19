from flask import Flask, render_template, session, redirect, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'hello1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

items = [
    {'id':'item1', 'name':'햄버거', 'price':3000},
    {'id':'item2', 'name':'핫도그', 'price':2000},
    {'id':'item3', 'name':'콜라', 'price':1500},
]

@app.route('/')
def index():
    return render_template('product.html', items=items) # 여기 상품 채워넣기

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    print('장바구니에 담을 상품: ', item_id)
    if 'cart' not in session:
        session['cart'] = {}

    if item_id in session['cart']:
        session['cart'][item_id] += 1
    else:
        # 장바구니에 담을 상품이 실제로 존재하는가?
        session['cart'][item_id] = 1

    session.modified = True # 세션 데이터가 수정되었음을 flask에게 인식시켜준다.

    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
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

if __name__ == "__main__":
    app.run(debug=True)

# 백엔드에서 필요한 정보를 채워서 랜더링(SSR)해서 사용자 브라우저에 보여준다.
# 1. 상품 보여주기
# 2. 카트에 추가시 a 태그를 잘 확장해서 /add-to-cart 곳을 호출
# 3. 서버는 이걸 받아서 세션에 장바구니에 담을 내용 저장, session['cart'] = 정보담기
# 4. /cart를 요청할 때, 우리의 세션 내용을 가져다가 전달한다./세션에서 꺼내서 자료 구조 만들어서 전달  