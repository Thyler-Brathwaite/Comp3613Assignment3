from App.observers.observer_base import Observer
from App.database import db
from App.models.activityhistory import activityhistory
from App.models.accolade import Accolade
from App.models import Student, LoggedHours

class ActivityHistoryObserver(Observer):
    def update(self, subject, event_type, payload):
        if event_type == 'logged_hours' and isinstance(payload, LoggedHours):
            logged = payload
            student = Student.query.get(logged.student_id)
            if student:
                activity = activityhistory(
                    student_id=logged.student_id,
                    activity_name="Logged Hours Approval",
                    activity_date=logged.timestamp.date(),
                    activity_details=f"Approved {logged.hours} hours by Staff ID {logged.staff_id}"
                )
                db.session.add(activity)
                db.session.commit()
        if event_type == 'accolade_awarded' and hasattr(payload, 'title'):
            acclaim = payload
            student = Student.query.get(acclaim.student_id)
            if student:
                activity = activityhistory(
                    student_id=acclaim.student_id,
                    activity_name="New Accolade Awarded",
                    activity_date=acclaim.date_awarded.date(),
                    activity_details=f"Awarded accolade: {acclaim.title}"
                )
                db.session.add(activity)
                db.session.commit()

class AccoladeObserver(Observer):
    def update(self, subject, event_type, payload):
        if event_type != 'logged_hours':
            return
        logged = payload
        student = Student.query.get(logged.student_id)
        if not student:
            return
        total_hours = sum(l.hours for l in student.loggedhours if l.status == 'approved')
        milestones = {
            10: "10 Hours Milestone",
            25: "25 Hours Milestone",
            50: "50 Hours Milestone"
        }
        for hours_needed, title in milestones.items():
            already = any(a.title == title for a in student.accolades)
            if total_hours >= hours_needed and not already:
                new_acc = Accolade(student_id=student.student_id, title=title)
                db.session.add(new_acc)
                db.session.commit()
                student.accolades.append(new_acc)
                db.session.commit()
                subject.notify_observers('accolade_awarded', new_acc)
