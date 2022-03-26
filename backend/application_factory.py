from flask import Flask
from .extensions import db, sock, ma, cors
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

DATABASE_URL = os.environ.get('DATABASE_URI')


def create_app():
    flask_app = Flask(__name__)

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(flask_app)
    ma.init_app(flask_app)
    cors.init_app(flask_app)
    sock.init_app(flask_app)

    return flask_app
