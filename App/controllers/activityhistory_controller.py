import datetime
from App.database import db
from App.models import activityhistory, Student, LoggedHours

def notify(id):
    LoggedHours=LoggedHours.query.get(id)
    
    add_hours_activity
    
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
        student.activityhistories.append(activity)
        
       

    

def add_accolade_activity(student_id,accolade):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity = activityhistory(
        student_id=student.student_id,
        activity_name="New Accolade Awarded",
        activity_date= accolade.date_awarded,
        activity_details=f"Awarded accolade: {accolade.accolade_name}"
    )
    db.session.add(activity)
    db.session.commit()
    return activity

        


    
    
