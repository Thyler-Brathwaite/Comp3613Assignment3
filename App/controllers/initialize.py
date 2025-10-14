from App.models import Student, Staff, Request,User
from App.controllers.student_controller import register_student
from App.controllers.staff_controller import register_staff
from App.controllers.user import create_user
from App.database import db


def initialize():


    db.drop_all()
    db.create_all()
    #create_user('bob', 'bobpass')

    # Add sample students

    users = [
        create_user('alice', 'alicepass'),
        create_user('bob', 'bobpass'),
        create_user('charlie', 'charliepass'),
        create_user('diana', 'dianapass'),
        create_user('eve', 'evepass'),
        create_user('frank', 'frankpass'),
        create_user('grace', 'gracepass'),     
        create_user('Mr. Smith', 'smithpass'),
        create_user('Ms. Johnson', 'johnsonpass'),
        create_user('Mr. Lee', 'leepass'),
    ]
    db.session.add_all(users)
    db.session.commit()
    
    students = [
        register_student('Alice', 'alice.smith@gmail.com', 1),
        register_student('Bob', 'bob.jones@hotmail.com', 2),
        register_student('Charlie', 'charlie.brown@gmail.com', 3),
        register_student('Diana', 'diana.lee@hotmail.com', 4),
        register_student('Eve', 'eve.patel@gmail.com', 5),
        register_student('Frank', 'frank.miller@gmail.com', 6),
        register_student('Grace', 'grace.wilson@hotmail.com', 7),
    ]
    db.session.add_all(students)
    db.session.commit()

    # Add sample staff members
    staff_members = [
        register_staff('Mr. Smith', 'mr.smith@gmail.com', 8),
        register_staff('Ms. Johnson', 'ms.johnson@hotmail.com', 9),
        register_staff('Mr. Lee', 'mr.lee@gmail.com', 10),
    ]
    for staff_member in staff_members:
        db.session.add(staff_member)
    db.session.commit()

    # Add sample requests for students
    all_students = Student.query.order_by(Student.id).all()
    requests = []
    import random
    for i, student in enumerate(all_students):
        hours = random.randint(10, 60)
        req = Request(student_id=student.id, hours=hours, status='pending')
        requests.append(req)
    db.session.add_all(requests)
    db.session.commit()

    # Add sample logged hours (approve first 2 requests by first 3 staff)
    from App.models import LoggedHours
    all_staff = Staff.query.order_by(Staff.id).all()
    for i, req in enumerate(requests[:3]):
        staff_member = all_staff[i % len(all_staff)]
        if i < 2:
            req.status = 'approved'
            log = LoggedHours(student_id=req.student_id, staff_id=staff_member.id, hours=req.hours, status='approved')
            db.session.add(log)
        else:
            req.status = 'denied'
    db.session.commit()

    
    