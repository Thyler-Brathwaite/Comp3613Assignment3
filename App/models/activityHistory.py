# App/models/activityhistory.py
from App.database import db
from datetime import datetime

class ActivityHistory(db.Model):
    __tablename__ = "activityhistory"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, student_id, activity_type, description):
        self.student_id = student_id
        self.activity_type = activity_type
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }
        
    def __repr__(self):
        return f"[ActivityHistory ID={self.id} StudentID={self.student_id} Type={self.activity_type} Description={self.description}]"