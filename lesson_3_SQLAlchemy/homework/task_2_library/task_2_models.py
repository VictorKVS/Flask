from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    books = db.relationship('Books', backref='author', lazy=True)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
