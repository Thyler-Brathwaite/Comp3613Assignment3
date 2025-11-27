from App.database import db
from datetime import datetime

class Accolade(db.Model):
    __tablename__ = "accolade"

    accolade_id = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    title       = db.Column(db.String(120), nullable=False)
    date_awarded = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, student_id, title):
        self.student_id = student_id
        self.title = title

    def __repr__(self):
        return f"<Accolade {self.title} for Student {self.student_id}>"

    def get_json(self):
        return {
            "accolade_id": self.accolade_id,
            "student_id": self.student_id,
            "title": self.title,
            "date_awarded": self.date_awarded.isoformat()
        }
