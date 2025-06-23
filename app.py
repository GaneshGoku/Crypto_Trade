from flask import Flask, render_template, request
from bot import BasicBot

app = Flask(__name__)
bot = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global bot
    result = None

    if request.method == 'POST':
        if not bot:
            bot = BasicBot(request.form['api_key'], request.form['api_secret'])

        order_type = request.form['order_type']
        symbol = request.form['symbol'].upper()
        side = request.form['side']
        quantity = float(request.form['quantity'])

        if order_type == 'market':
            result = bot.place_market_order(symbol, side, quantity)
        elif order_type == 'limit':
            price = request.form['price']
            result = bot.place_limit_order(symbol, side, quantity, price)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
