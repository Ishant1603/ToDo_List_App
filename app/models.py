from app import db
from flask_login import UserMixin
from datetime import datetime

class Todo(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    planned_date = db.Column(db.Date, nullable=True)
    planned_time = db.Column(db.Time, nullable=True)
    notified = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"{self.SNo} - {self.title}"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class CompletedTodo(db.Model):
    __tablename__ = 'completed_todos'
    CompleteId = db.Column(db.Integer, primary_key=True)
    SNo = db.Column(db.Integer, db.ForeignKey('todo.SNo'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    planned_date = db.Column(db.Date, nullable=True)
    planned_time = db.Column(db.Time, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<CompletedTodo {self.title}>"
