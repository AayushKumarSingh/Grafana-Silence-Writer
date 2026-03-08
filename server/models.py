from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class RequestLogs(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="NA")
    matchers = db.Column(db.Text)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    comment = db.Column(db.Integer)
    silenceID = db.Column(db.String(50), default="NA")
    failReason = db.Column(db.Text, default="")


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    team = db.Column(db.String(50), nullable=False)
    folder_access = db.Column(db.String(100), nullable=False)
