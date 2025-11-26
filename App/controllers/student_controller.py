import datetime
from App.database import db
from App.models import User,Staff,Student,Request,accolade

def register_student(name,email,password):
    new_student=Student.create_student(name,email,password)
    return new_student

def get_approved_hours(student_id): #calculates and returns the total approved hours for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    return total_hours

def create_hours_request(student_id,hours): #creates a new hours request for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    req = student.request_hours_confirmation(hours)
    return req

def fetch_requests(student_id): #fetch requests for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    return student.requests

def fetch_accolades(student_id): #fetch accolades for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    accolades = student.accolades()
    return accolades

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

def check_accolade_eligibility(student_id  ):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    total_hours = student.get_approved_hours()
    
    
    if total_hours >= 10:
        new_accolade = accolade(
            student_id=student.student_id,
            accolade_name="10 Hours Milestone",
            date_awarded=datetime.datetime.utcnow().date()
        )
        db.session.add(new_accolade)
    student.accolades.append(new_accolade)
    db.session.commit()
    
    if total_hours >= 25:
        new_accolade = accolade(
            student_id=student.student_id,
            accolade_name="25 Hours Milestone",
            date_awarded=datetime.datetime.utcnow().date()
        )
        db.session.add(new_accolade)
        student.accolades.append(new_accolade)
        
        
    if total_hours >= 50:
        new_accolade = accolade(
            student_id=student.student_id,
            accolade_name="50 Hours Milestone",
            date_awarded=datetime.datetime.utcnow().date()
        )
        db.session.add(new_accolade)
        student.accolades.append(new_accolade)
        
        db.session.commit()    
        
    
    

def get_all_students_json():
    students = Student.query.all()
    return [student.get_json() for student in students]

