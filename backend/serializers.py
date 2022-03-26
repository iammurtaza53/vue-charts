from .extensions import ma
from marshmallow import fields

class TestSchema(ma.Schema):
    __tablename__ = "test"
    testid = fields.Integer(dump_only=True)
    ticker = fields.String()
    date = fields.Integer()
    price = fields.Integer()

test_schema = TestSchema()
tests_schema = TestSchema(many=True)


class EarningsdatesSchema(ma.Schema):
    __tablename__ = "earningsdates"
    earningsdateid = fields.Integer(dump_only=True)
    ticker = fields.String()
    exactearningsdate = fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    averageoptionvol = fields.Integer()
    averagestockvol = fields.Integer()
    marketcap = fields.Integer()
    impliedmove = fields.Float()
    staticstrike = fields.Float()
    staticprice = fields.Float()
    staticexpiry = fields.String()
    staticunderlying = fields.Float()
    staticiv = fields.Float()
    actualmove = fields.Float()


earning_schema = EarningsdatesSchema()
earnings_schema = EarningsdatesSchema(many=True)



class ChangesSchema(ma.Schema):
    __tablename__ = "changes"
    changesid = fields.Integer(dump_only=True)
    ticker = fields.String()
    dated = fields.DateTime(format='%Y-%m-%dT%H:%M:%S%z')
    iv = fields.Float()
    straddle = fields.Float()
    impliedmove = fields.Float()
    underlying = fields.Float()
    strike = fields.Float()
    quarter = fields.String()


change_schema = ChangesSchema()
changes_schema = ChangesSchema(many=True)
