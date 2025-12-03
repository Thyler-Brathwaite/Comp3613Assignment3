from App.database import db
from datetime import datetime

class ActivityHistory(db.Model):
    __tablename__ = "activityhistory"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    def __init__(self, student_id, activity_type, description, timestamp=None):
        self.student_id = student_id
        self.activity_type = activity_type
        self.description = description
        self.timestamp = timestamp or datetime.utcnow()
 
    def get_json(self):

        ts = self.timestamp or datetime.utcnow()
        return {
            'id': self.id,
            'student_id': self.student_id,
            'activity_type': self.activity_type,
            'description': self.description,
            'timestamp': ts.isoformat()
        }

    def __repr__(self):
        return (
            f"[ActivityHistory ID={self.id} "
            f"StudentID={self.student_id} "
            f"Type={self.activity_type} "
            f"Description={self.description}]"
        )
 