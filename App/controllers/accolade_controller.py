from App.database import db
from App.models import Accolade, Student

def fetch_accolades_for_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    return student.accolades

def create_accolade(student_id, title):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    new_acc = Accolade(student_id=student_id, title=title)
    db.session.add(new_acc)
    db.session.commit()
    return new_acc
