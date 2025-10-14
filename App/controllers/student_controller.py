from App.database import db
from App.models import User,Staff,Student,Request

def register_student(name,email,user_id): #register a new student
    new_student=Student.create_student(name,email,user_id)
    return new_student

def get_approved_hours(student_id): #calculates and returns the total approved hours for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    return (student.name,total_hours)

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
            'name': student.name,
            'hours': total_hours
        })

    leaderboard.sort(key=lambda item: item['hours'], reverse=True)

    return leaderboard

def get_all_students(): #fetch all students
    return db.session.scalars(db.select(Student)).all()

def get_all_students_json(): #fetch all students in json format
    students = get_all_students()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students