from App.database import db
from datetime import datetime

class accolade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    accolade_name = db.Column(db.String(100), nullable=False)
    date_awarded = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, student_id, accolade_name):
        self.student_id = student_id
        self.accolade_name = accolade_name

    def __repr__(self):
        return f"[Accolade ID={self.id} StudentID={self.student_id} Accolade={self.accolade_name} Date Awarded={self.date_awarded}]"

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'accolade_name': self.accolade_name,
            'date_awarded': self.date_awarded.isoformat()
        }