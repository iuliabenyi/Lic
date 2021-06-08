from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class UserPage(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    userId = db.Column(db.Integer)
    userName = db.Column(db.String)
    userTags = db.Column(db.String)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    mainTag = db.Column(db.String(1000))

class UsersAll(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    type = db.Column(db.String(1000))
    mainTag = db.Column(db.String(1000))
    lastLogin = db.Column(db.String((100)))

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    nameUser = db.Column(db.String(1000))
    nameTherapist = db.Column(db.String(1000))
    message = db.Column(db.String(5000))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    nameReceiver = db.Column(db.String(1000))
    nameSender = db.Column(db.String(1000))
    message = db.Column(db.String(5000))

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    nameReceiver = db.Column(db.String(1000))
    nameSender = db.Column(db.String(1000))
    notification = db.Column(db.Boolean)