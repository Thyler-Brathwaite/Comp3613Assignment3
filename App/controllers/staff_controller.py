from App.database import db
from App.models import User, Staff, Student, Request

def register_staff(name,email,password):
    new_staff = Staff.create_staff(name, email, password)
    return new_staff

def fetch_all_requests():
    pending_requests = Request.query.filter_by(status='pending').all()
    if not pending_requests:
        return []

    requests_data=[]
    for req in pending_requests:
        student = Student.query.get(req.student_id)
        student_name = student.username if student else "Unknown"

        requests_data.append({
            'id': req.id,
            'student_name': student_name,
            'hours': req.hours,
            'status':req.status
        })

    return requests_data

def process_request_approval(staff_id, request_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")

    request = Request.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")

    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown"
    logged = staff.approve_request(request)

    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'logged_hours': logged
    }

def process_request_denial(staff_id, request_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")

    request = Request.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")

    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown"
    denied = staff.deny_request(request)

    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'denial_successful': denied
    }

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

def get_all_staff_json():
    staff_members = Staff.query.all()
    return [staff.get_json() for staff in staff_members]
