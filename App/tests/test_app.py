import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Request, Staff, LoggedHours, ActivityHistory

from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)

from App.controllers.student_controller import (
    register_student,
    create_hours_request,
    fetch_requests,
    get_approved_hours,
    fetch_accolades,
    generate_leaderboard
)

from App.controllers.staff_controller import (
    register_staff,
    fetch_all_requests,
    process_request_approval,
    process_request_denial
)

LOGGER = logging.getLogger(__name__)

#  UNIT TESTS 

class UserUnitTests(unittest.TestCase):

    def test_check_password(self):
        Testuser = User("David Goggins", "goggs@gmail.com", "goggs123", "student")
        self.assertTrue(Testuser.check_password("goggs123"))

    def test_set_password(self):
        password = "passtest"
        new_password = "passtest"
        Testuser = User("bob", "bob@email.com", password, "user")
        Testuser.set_password(new_password)
        assert Testuser.check_password(new_password)


class StaffUnitTests(unittest.TestCase):

    def test_init_staff(self):
        newstaff = Staff("Jacob Lester", "jacob55@gmail.com", "Jakey55")
        self.assertEqual(newstaff.username, "Jacob Lester")
        self.assertEqual(newstaff.email, "jacob55@gmail.com")
        self.assertTrue(newstaff.check_password("Jakey55"))

    def test_staff_get_json(self):
        Teststaff = Staff("Jacob Lester", "jacob55@gmail.com", "jakey55")
        staff_json = Teststaff.get_json()
        self.assertEqual(staff_json['username'], "Jacob Lester")
        self.assertEqual(staff_json['email'], "jacob55@gmail.com")

    def test_repr_staff(self):
        Teststaff = Staff("Jacob Lester", "jacob55@gmail.com", "jakey55")
        rep = repr(Teststaff)
        self.assertIn("Staff ID=", rep)
        self.assertIn("Name=", rep)
        self.assertIn("Email=", rep)
        self.assertIn("Jacob Lester", rep)
        self.assertIn("jacob55@gmail.com", rep)


class StudentUnitTests(unittest.TestCase):

    def test_init_student(self):
        newStudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        self.assertEqual(newStudent.username, "David Moore")
        self.assertEqual(newStudent.email, "david77@outlook.com")
        self.assertTrue(newStudent.check_password("iloveschool67"))

    def test_student_get_json(self):
        newstudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        student_json = newstudent.get_json()
        self.assertEqual(student_json['username'], "David Moore")
        self.assertEqual(student_json['email'], "david77@outlook.com")

    def test_repr_student(self):
        newstudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        rep = repr(newstudent)
        self.assertIn("Student ID=", rep)
        self.assertIn("Name=", rep)
        self.assertIn("Email=", rep)
        self.assertIn("David Moore", rep)
        self.assertIn("david77@outlook.com", rep)


class StudentObserverUnitTests(unittest.TestCase):

    def test_update_on_approved_hours_notifies_observer(self):

        class DummyObserver:
            def __init__(self):
                self.events = []

            def update(self, event_type, payload):
                self.events.append((event_type, payload))

        student = Student("Alex King", "alex@example.com", "pass123")
        observer = DummyObserver()

        student.attach(observer)

        log = LoggedHours(student_id=1, staff_id=2, hours=3.0, status="approved")

        student.update_on_approved_hours(log)

        self.assertEqual(len(observer.events), 1)
        event_type, payload = observer.events[0]

        self.assertEqual(event_type, "logged_hours")
        self.assertIs(payload, log)


class RequestUnitTests(unittest.TestCase):

    def test_init_request(self):
        Testrequest = Request(student_id=12, hours=30, status='pending')
        self.assertEqual(Testrequest.student_id, 12)
        self.assertEqual(Testrequest.hours, 30)
        self.assertEqual(Testrequest.status, 'pending')

    def test_repr_request(self):
        Testrequest = Request(student_id=4, hours=40, status='denied')
        rep = repr(Testrequest)
        self.assertIn("RequestID=", rep)
        self.assertIn("StudentID=", rep)
        self.assertIn("Hours=", rep)
        self.assertIn("Status=", rep)


class LoggedHoursUnitTests(unittest.TestCase):

    def test_init_loggedhours(self):
        Testlogged = LoggedHours(student_id=1, staff_id=2, hours=20, status='approved')
        self.assertEqual(Testlogged.student_id, 1)
        self.assertEqual(Testlogged.staff_id, 2)
        self.assertEqual(Testlogged.hours, 20)
        self.assertEqual(Testlogged.status, 'approved')

    def test_repr_loggedhours(self):
        Testlogged = LoggedHours(student_id=1, staff_id=2, hours=20, status='approved')
        rep = repr(Testlogged)
        self.assertIn("Log ID=", rep)
        self.assertIn("StudentID =", rep)
        self.assertIn("Approved By (StaffID)=", rep)
        self.assertIn("Hours Approved=", rep)


class ActivityHistoryUnitTests(unittest.TestCase):

    def test_init_activity_history(self):
        history = ActivityHistory(
            student_id=1,
            activity_type="Login",
            description="Student logged in"
        )
        self.assertEqual(history.student_id, 1)
        self.assertIsNotNone(history.timestamp)

    def test_get_json_activity_history(self):
        history = ActivityHistory(
            student_id=2,
            activity_type="Request Created",
            description="Requested 5 hours"
        )
        data = history.get_json()
        self.assertEqual(data["student_id"], 2)
        self.assertIn("timestamp", data)

    def test_repr_activity_history(self):
        history = ActivityHistory(
            student_id=3,
            activity_type="Accolade Earned",
            description="Accolade earned: 10 Hours Milestone"
        )
        rep = repr(history)
        self.assertIn("ActivityHistory ID=", rep)
        self.assertIn("StudentID=3", rep)


#        INTEGRATION TESTS (MARKED)

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()



class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        staff = register_staff("marcus", "marcus@example.com", "pass123")
        assert staff.username == "marcus"

    def test_request_fetch(self):
        student = Student.create_student("tariq", "tariq@example.com", "studpass")
        req = Request(student_id=student.student_id, hours=3.5, status='pending')
        db.session.add(req)
        db.session.commit()
        requests = fetch_all_requests()
        assert any(r['student_name'] == 'tariq' for r in requests)

    def test_hours_approval(self):
        staff = register_staff("carmichael", "carm@example.com", "staffpass")
        student = Student.create_student("niara", "niara@example.com", "studpass")
        req = Request(student_id=student.student_id, hours=2.0, status='pending')
        db.session.add(req)
        db.session.commit()
        result = process_request_approval(staff.staff_id, req.id)
        assert result['request'].status == 'approved'


    def test_hours_denial(self):
        staff = register_staff("maritza", "maritza@example.com", "staffpass")
        student = Student.create_student("jabari", "jabari@example.com", "studpass")
        req = Request(student_id=student.student_id, hours=1.0, status='pending')
        db.session.add(req)
        db.session.commit()
        result = process_request_denial(staff.staff_id, req.id)
        assert result['request'].status == 'denied'



class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student = register_student("junior", "junior@example.com", "studpass")
        assert student.username == "junior"

    def test_request_hours_confirmation(self):
        student = Student.create_student("amara", "amara@example.com", "pass")
        req = create_hours_request(student.student_id, 4.0)
        assert req.status == 'pending'

    def test_fetch_requests(self):
        student = Student.create_student("kareem", "kareem@example.com", "pass")
        create_hours_request(student.student_id, 1.0)
        create_hours_request(student.student_id, 2.5)
        reqs = fetch_requests(student.student_id)
        assert len(reqs) >= 2

    def test_get_approved_hours_and_accolades(self):
        student = Student.create_student("nisha", "nisha@example.com", "pass")
        lh1 = LoggedHours(student_id=student.student_id, staff_id=None, hours=6.0, status='approved')
        lh2 = LoggedHours(student_id=student.student_id, staff_id=None, hours=5.0, status='approved')
        db.session.add_all([lh1, lh2])
        db.session.commit()
        total = get_approved_hours(student.student_id)
        assert total == 11.0

    def test_generate_leaderboard(self):
        a = Student.create_student("zara", "zara@example.com", "p")
        b = Student.create_student("omar", "omar@example.com", "p")
        c = Student.create_student("leon", "leon@example.com", "p")
        db.session.add_all([
            LoggedHours(student_id=a.student_id, staff_id=None, hours=10.0, status='approved'),
            LoggedHours(student_id=b.student_id, staff_id=None, hours=5.0, status='approved'),
            LoggedHours(student_id=c.student_id, staff_id=None, hours=1.0, status='approved')
        ])
        db.session.commit()
        leaderboard = generate_leaderboard()
        names = [item['name'] for item in leaderboard]
        assert names.index('zara') < names.index('omar') < names.index('leon')



class ActivityHistoryIntegrationTests(unittest.TestCase):

    def test_activity_history_created_on_hours_approval(self):
        staff = register_staff("staff_ah", "staff_ah@example.com", "pass123")
        student = Student.create_student("stud_ah", "stud_ah@example.com", "pass123")

        req = Request(student_id=student.student_id, hours=4.0, status='pending')
        db.session.add(req)
        db.session.commit()

        result = process_request_approval(staff.staff_id, req.id)

        assert result['request'].status == 'approved'

        entries = ActivityHistory.query.filter_by(
            student_id=student.student_id,
            activity_type="Hours Approved"
        ).all()

        assert len(entries) >= 1


    def test_accolade_activity_created_when_milestone_reached(self):
        staff = register_staff("staff_ac", "staff_ac@example.com", "pass123")
        student = Student.create_student("stud_ac", "stud_ac@example.com", "pass123")

        req = Request(student_id=student.student_id, hours=10.0, status='pending')
        db.session.add(req)
        db.session.commit()

        process_request_approval(staff.staff_id, req.id)

        accolades = ActivityHistory.query.filter_by(
            student_id=student.student_id,
            activity_type="Accolade Earned"
        ).all()

        assert len(accolades) >= 1
