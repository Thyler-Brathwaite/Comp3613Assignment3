from App.database import db
from App.models.loggedhours import LoggedHours
from .user import User
from App.observers.subject import Subject
from App.observers.activity_history_observer import ActivityHistoryObserver


class Student(User, Subject):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)

    loggedhours = db.relationship('LoggedHours', backref='student', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Request', backref='student', lazy=True, cascade="all, delete-orphan")
    activityhistories = db.relationship('activityhistory', backref='student', lazy=True, cascade="all, delete-orphan")
    

    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

    def __init__(self, username, email, password):
       super().__init__(username, email, password, role="student")
       self._observers = []
       Subject.__init__(self)

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
    
   
    newstudent.attach(ActivityHistoryObserver())

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

  def accolades(self):
        # Only count approved logged hours
        total_hours = self.get_total_hours()
        accolades = []
        if total_hours >= 10:
            accolades.append('10 Hours Milestone')
        if total_hours >= 25:
            accolades.append('25 Hours Milestone')
        if total_hours >= 50:
            accolades.append('50 Hours Milestone')
        return accolades

    def total_hours(self):
        return self.get_total_hours()

def update_on_approved_hours(self, logged_obj):
    self.notify_observers('logged_hours', logged_obj)
    self.check_and_notify_accolades()



def check_and_notify_accolades(self):
    current_accolades = set(self.accolades())  # recomputed
    history_accolades = {
        h.description.replace("Accolade earned: ", "")
        for h in self.activityhistories
        if h.activity_type == "Accolade Earned"
    }

    new_accolades = current_accolades - history_accolades

    for accolade in new_accolades:
        self.notify_observers("accolade_awarded", (self, accolade))



  
