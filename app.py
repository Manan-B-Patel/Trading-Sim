from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from data import *
from input import *
from api import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abd85f27368f87eb619cb3e384a48eb8'


@app.route('/', methods = ['GET', 'POST'])
@app.route('/output', methods = ['GET', 'POST'])
def output():
    form = StockListForm()
    if form.validate_on_submit():
        stock = form.stock.data
        interval = form.interval.data
        return redirect(url_for('dashboard', stock = stock, interval = interval))
    return render_template('output.html', form = form, title = 'Output')

@app.route('/dashboard/<stock>/<interval>', methods=['GET', 'POST'])
@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard(stock, interval):
    stockInfo = getData(stock)
    form = SharesForm()
    sell = Sell()
    if form.validate_on_submit():
            numShares = form.shares.data
            boughtPrice = 10
            isSubmit = True
    elif sell.validate_on_submit():
            numShares = 0
            boughtPrice = 0
            isSubmit = False
    else:
        boughtPrice = 0
        numShares = 0
        isSubmit = False
        
    return render_template('dashboard.html', isSubmit = isSubmit, numShares = numShares, sell = sell, form = form, stockInfo = stockInfo, stock = stock, interval = interval,
                           boughtPrice = boughtPrice)

@app.route('/graph/<stock>/<interval>', methods=['GET'])
@app.route('/graph/', methods=['GET'])
def graph(stock, interval):
    list, list2 = api_call(stock, interval)
    return jsonify({"1": list, "2": list2})

@app.route('/predict/<stock>/<interval>', methods=['GET'])
@app.route('/predict/', methods=['GET'])
def predict(stock, interval):
    api_call(stock, interval)
    json_response = future()
    return jsonify(json_response)
        
if __name__ == "__main__":
    app.run(debug = True)