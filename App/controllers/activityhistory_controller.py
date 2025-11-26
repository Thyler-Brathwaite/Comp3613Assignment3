import datetime
from App.database import db
from App.models import activityhistory, Student, LoggedHours

def add_hours_activity(stduen_id):
    student = Student.query.get(stduen_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    

        student_id=student.student_id,
        activity_name="New Accolade Awarded",
        activity_date=datetime.datetime.utcnow().date(),
        activity_details=f"Accolade awarded to Student ID {student.student_id}"
    )
    db.session.add(activity)
    db.session.commit()
    return activity
    
    
