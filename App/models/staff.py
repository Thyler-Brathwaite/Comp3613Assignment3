from App.database import db
from .user import User
from App.models.loggedhours import LoggedHours
from App.models.student import Student


class Staff(User):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    loggedhours = db.relationship('LoggedHours', backref='staff', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }

    def __init__(self, username, email, password):
       super().__init__(username, email, password, role="staff")

    def __repr__(self):
        return f"[Staff ID= {str(self.staff_id):<3} Name= {self.username:<10} Email= {self.email}]"

    def get_json(self):
        return{
            'staff_id': self.staff_id,
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def create_staff(username, email, password):
        newstaff = Staff(username=username, email=email, password=password)
        db.session.add(newstaff)
        db.session.commit()
        return newstaff

    def approve_request(self, request):
        from App.models import LoggedHours
        if request.status != 'pending':
            return None
        request.status = 'approved'
        logged = LoggedHours(student_id=request.student_id, staff_id=self.staff_id, hours=request.hours, status='approved')
        db.session.add(logged)
        db.session.commit()
        student = Student.query.get(request.student_id)
        if student:
            student.update_on_approved_hours(logged)
        return logged

    def deny_request(self, request):
        if request.status != 'pending':
            return False
        request.status = 'denied'
        db.session.commit()
        return True
