from App.database import db
from datetime import datetime

from wsgi import hours

class activityhistory(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    activity_name = db.Column(db.String(100), nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    activity_details = db.Column(db.String(255), nullable=True)
   

    def __init__(self, student_id, activity_name, activity_date, activity_details=None):
        self.student_id = student_id
        self.activity_name = activity_name
        self.activity_date = activity_date
        self.activity_details = activity_details
        
        
    def __repr__(self):
        return f"[Activity ID={self.id} StudentID={self.student_id} Activity Name={self.activity_name} Date={self.activity_date}]"
    
    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'activity_name': self.activity_name,
            'activity_date': self.activity_date.isoformat(),
            'activity_details': self.activity_details,
            
        }
        
        
