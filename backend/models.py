from datetime import datetime
from .extensions import db


class Test(db.Model):
    testid = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20))
    date = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, ticker, date, price):
        self.ticker = ticker
        self.date = date
        self.price = price



class Earningsdates(db.Model):
    earningsdateid = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(15))
    exactearningsdate = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.now)
    averageoptionvol = db.Column(db.Integer)
    averagestockvol = db.Column(db.Integer)
    marketcap = db.Column(db.Integer)
    impliedmove = db.Column(db.Float)
    staticstrike = db.Column(db.Float)
    staticexpiry = db.Column(db.String(12))
    staticprice = db.Column(db.Float)
    staticunderlying = db.Column(db.Float)
    staticiv = db.Column(db.Float)
    actualmove = db.Column(db.Float)

    def __init__(self, ticker, exactearningsdate, averageoptionvol, averagestockvol, marketcap, impliedmove, staticstrike, staticexpiry, staticprice, staticunderlying, staticiv, actualmove):
        self.ticker = ticker
        self.exactearningsdate = exactearningsdate
        self.averageoptionvol = averageoptionvol
        self.averagestockvol = averagestockvol
        self.marketcap = marketcap
        self.impliedmove = impliedmove
        self.staticstrike = staticstrike
        self.staticprice = staticprice
        self.staticexpiry = staticexpiry
        self.staticunderlying = staticunderlying
        self.staticiv = staticiv
        self.actualmove = actualmove


class Changes(db.Model):
    changesid = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(15))
    dated = db.Column(db.DateTime, default=datetime.utcnow,
                      onupdate=datetime.now)
    iv = db.Column(db.Float)
    straddle = db.Column(db.Float)
    impliedmove = db.Column(db.Float)
    underlying = db.Column(db.Float)
    strike = db.Column(db.Float)
    quarter = db.Column(db.String(2))

    def __init__(self, ticker, dated, iv, straddle, impliedmove, underlying, strike, quarter):
        self.ticker = ticker
        self.dated = dated
        self.iv = iv
        self.straddle = straddle
        self.impliedmove = impliedmove
        self.underlying = underlying
        self.strike = strike
        self.quarter = quarter
