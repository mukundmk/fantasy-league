from flask import Flask

__author__ = 'mukundmk'


app = Flask(__name__)
app.config.from_pyfile('config.py')

from app import views