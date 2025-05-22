from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)  # optional but good to require text
    complete = db.Column(db.Boolean, default=False)  # set a default for convenience

    def __repr__(self):
        return f"<Todo {self.text}>"
