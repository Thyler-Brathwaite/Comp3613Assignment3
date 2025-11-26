import datetime
from App.database import db
from App.models import activityhistory, Student, LoggedHours

def add_hours_activity(loggedhours):
    student = Student.query.get(loggedhours.student_id)
    if student:
        activity = activityhistory(
            student_id=loggedhours.student_id,
            activity_name="Logged Hours Approval",
            activity_date=loggedhours.timestamp.date(),
            activity_details=f"Approved {loggedhours.hours} hours by Staff ID {loggedhours.staff_id}"   
        )
        db.session.add(activity)
        db.session.commit()
        return activity
    else:
        raise ValueError("Student not found for the given logged hours.")
    

def add_accolade_activity(student):
    activity = activityhistory(
        student_id=student.student_id,
        activity_name="New Accolade Awarded",
        activity_date=datetime.datetime.utcnow().date(),
        activity_details=f"Accolade awarded to Student ID {student.student_id}"
    )
    db.session.add(activity)
    db.session.commit()
    return activity
    
    
