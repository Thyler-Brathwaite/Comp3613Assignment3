from App.database import db
from App.models import activityhistory, Student

def get_activity_history_for_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    activities = activityhistory.query.filter_by(student_id=student_id).order_by(activityhistory.activity_date.desc()).all()
    return activities

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

def add_accolade_activity(student_id, accolade_obj):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    activity = activityhistory(
        student_id=student.student_id,
        activity_name="New Accolade Awarded",
        activity_date= accolade_obj.date_awarded.date(),
        activity_details=f"Awarded accolade: {accolade_obj.title}"
    )
    db.session.add(activity)
    db.session.commit()
    return activity
