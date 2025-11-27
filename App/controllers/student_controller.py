import datetime
from App.database import db
from App.models import User, Staff, Student, Request, Accolade, LoggedHours

def register_student(name,email,password):
    new_student=Student.create_student(name,email,password)
    return new_student

def get_approved_hours(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    return total_hours

def create_hours_request(student_id,hours):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    req = student.request_hours_confirmation(hours)
    return req

def fetch_requests(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    return student.requests

def fetch_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    return student.accolades

def generate_leaderboard():
    students = Student.query.all()
    leaderboard = []
    for student in students:
        total_hours=sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
        leaderboard.append({
            'name': student.username,
            'hours': total_hours
        })
    leaderboard.sort(key=lambda item: item['hours'], reverse=True)
    return leaderboard

def check_accolade_eligibility(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    total_hours = student.get_total_hours()
    milestones = {
        10:  "10 Hours Milestone",
        25:  "25 Hours Milestone",
        50:  "50 Hours Milestone",
    }

    for hours, name in milestones.items():
        already = any(a.title == name for a in student.accolades)
        if total_hours >= hours and not already:
            new_acc = Accolade(
                student_id=student_id,
                title=name
            )
            db.session.add(new_acc)
            db.session.commit()

def update(student_id, hours):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    student.request_hours_confirmation(hours)
    db.session.commit()

def get_all_students_json():
    students = Student.query.all()
    return [student.get_json() for student in students]
