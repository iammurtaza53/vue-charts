from flask import request, jsonify, session
import json
import time
from .application_factory import create_app
from .extensions import db, sock
from .serializers import *
from .models import Earningsdates, Changes, Test

app = create_app()

# REST APIS


@app.route('/add-earning', methods=['POST'])
def create_earning():
    data = request.json
    ticker = data['ticker']
    exactearningsdate = data['exactearningsdate']
    averageoptionvol = data['averageoptionvol']
    averagestockvol = data['averagestockvol']
    marketcap = data['marketcap']
    impliedmove = data['impliedmove']
    staticstrike = data['staticstrike']
    staticprice = data['staticprice']
    staticexpiry = data['staticexpiry']
    staticunderlying = data['staticunderlying']
    staticiv = data['staticiv']
    actualmove = data['actualmove']

    new_earning = Earningsdates(ticker, exactearningsdate, averageoptionvol, averagestockvol, marketcap,
                                impliedmove, staticstrike, staticprice, staticexpiry, staticunderlying, staticiv, actualmove)
    db.session.add(new_earning)
    db.session.commit()
    return earning_schema.jsonify(new_earning)


@app.route('/add-change', methods=['POST'])
def add_change():
    data = request.json
    ticker = data['ticker']
    dated = data['dated']
    iv = data['iv']
    straddle = data['straddle']
    impliedmove = data['impliedmove']
    underlying = data['underlying']
    strike = data['strike']
    quarter = data['quarter']

    new_change = Changes(ticker, dated, iv, straddle,
                         impliedmove, underlying, strike, quarter)
    db.session.add(new_change)
    db.session.commit()
    return change_schema.jsonify(new_change)


@app.route('/add-test', methods=['POST'])
def create_test():
    data = request.json
    ticker = data['ticker']
    date = data['date']
    price = data['price']
    new_test = Test(ticker, date, price)
    db.session.add(new_test)
    db.session.commit()
    return test_schema.jsonify(new_test)


@app.route('/get-all-earnings', methods=['GET'])
def get_earnings():
    all_earnings = Earningsdates.query.all()
    result = earnings_schema.dump(all_earnings)
    return jsonify(result)


@app.route('/get-earning-by-id/<id>', methods=['GET'])
def get_earning_by_id(id):
    get_earning = db.session.query(Earningsdates).order_by(
        Earningsdates.exactearningsdate.asc()).offset(id).first()
    earning = earning_schema.dump(get_earning)
    return earning


@app.route('/get-all-changes/<ticker>', methods=['GET'])
def get_changes(ticker):
    all_changes = Changes.query.filter(Changes.ticker==ticker).order_by(Changes.dated).all()
    result = changes_schema.dump(all_changes)
    return jsonify(result)


@app.route('/get-last-changes/<ticker>', methods=['GET'])
def get_last_changes(ticker):
    last_item = Changes.query.filter(Changes.ticker==ticker).order_by(Changes.changesid.desc()).first()
    result = change_schema.dump(last_item)
    return jsonify(result)


@app.route('/get-all-tests', methods=['GET'])
def get_tests():
    all_tests = Test.query.all()
    result = tests_schema.dump(all_tests)
    return jsonify(result)


@app.route('/get-test-by-id/<id>', methods=['GET'])
def get_test_by_id(id):
    get_test = Test.query.get(id)
    test = test_schema.dump(get_test)
    return test


@app.route('/get-unique-tickers', methods=['GET'])
def get_unique_tickers():
    query = db.session.query(Changes.ticker.distinct().label("ticker"))
    tickers = [row.ticker for row in query.all()]
    return jsonify(tickers)


# Sockets Connection
@sock.route('/get-updated-earnings')
def get_update_earnings(ws):
    try:
        earning = ws.receive()
        earning = json.loads(earning)
        db.session.commit()
        ws.send(earning)
        time.sleep(20)
        ws.close()

    except Exception as e:
        print(e)
        print("I am closing now due to: ", str(e))
        ws.close()


@sock.route('/get-updated-data')
def get_update_data(ws):

    total = 45  # total rows in db

    try:
        for i in range(1, total):
            time.sleep(1)
            obj = get_earning_by_id(i)
            obj = json.dumps(obj)
            ws.send(obj)

        time.sleep(2)
        ws.close()

    except Exception as e:
        print(e)
        print("I am closing now due to: ", str(e))
        ws.close()


if __name__ == "__main__":
    app.run(debug=True)
