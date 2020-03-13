from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# SQLALCHEMY_DATABASE_URI ="postgresql://project1:project1@localhost/project1"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = "./app/static/uploads"
SECRET_KEY = 'Sup3r$3cretkey'
SQLALCHEMY_DATABASE_URI='postgres://ljdaplxbetluhc:220d2f83502f7238b071107768169c5f59b3077fa78805c794311d0d60fe6c28@ec2-34-206-252-187.compute-1.amazonaws.com:5432/dee35cq710ood1'
app.config.from_object(__name__)

db = SQLAlchemy(app)

from app import views
