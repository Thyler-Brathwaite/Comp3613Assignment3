from App.database import db
from App.models.loggedhours import LoggedHours
from .user import User

class Student(User):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    loggedhours = db.relationship('LoggedHours', backref='student', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Request', backref='student', lazy=True, cascade="all, delete-orphan")
    activityhistories = db.relationship('activityhistory', backref='student', lazy=True, cascade="all, delete-orphan")
    accolades = db.relationship('Accolade', backref='student', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

    def __init__(self, username, email, password):
       super().__init__(username, email, password, role="student")
       self._observers = []

    def __repr__(self):
        return f"[Student ID= {str(self.student_id):<3}  Name= {self.username:<10} Email= {self.email}]"

    def get_json(self):
        return{
            'student_id': self.student_id,
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def create_student(username, email, password):
        newstudent = Student(username=username, email=email, password=password)
        db.session.add(newstudent)
        db.session.commit()
        return newstudent

    def request_hours_confirmation(self, hours):
        from App.models import Request
        request = Request(student_id=self.student_id, hours=hours, status='pending')
        db.session.add(request)
        db.session.commit()
        return request

    def get_total_hours(self):
        total = 0
        for log in self.loggedhours:
            if log.status == 'approved':
                total += log.hours
        return total

    def total_hours(self):
        return self.get_total_hours()

    def attach_observer(self, observer):
        if not hasattr(self, "_observers"):
            self._observers = []
        if observer not in self._observers:
            self._observers.append(observer)

    def detach_observer(self, observer):
        if hasattr(self, "_observers") and observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type, payload):
        if not hasattr(self, "_observers"):
            self._observers = []
        for obs in list(self._observers):
            try:
                obs.update(self, event_type, payload)
            except Exception:
                pass

    def update_on_approved_hours(self, logged_hours):
        self.notify_observers('logged_hours', logged_hours)
