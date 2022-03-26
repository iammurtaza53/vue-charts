from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_sock import Sock
 

db = SQLAlchemy()
ma = Marshmallow()
cors = CORS(supports_credentials=True)
sock = Sock()