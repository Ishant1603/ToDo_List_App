from app import db
from datetime import datetime
class Todo(db.Model):
    SNo = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    Date_created = db.Column(db.DateTime,default = datetime.utcnow)

    def __repr__(self) -> str :
        return f"{self.SNo} - {self.title}"
