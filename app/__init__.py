from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

file_path = os.path.join(os.getcwd(), 'todo.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f3b9c6d2e8e84a3e9a1f2c07a9e3b4d7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
