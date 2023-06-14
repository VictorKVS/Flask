from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    marks = db.relationship('Mark', backref='student', lazy=True)


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), unique=True, nullable=False)
    mark = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
