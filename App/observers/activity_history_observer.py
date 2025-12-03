# App/observers/activity_history_observer.py

from App.database import db

class ActivityHistoryObserver:
    def update(self, event_type, data):
        """
        event_type: string ("logged_hours", "milestone", etc.)
        data: object passed from Subject
        """
        from App.models import ActivityHistory, LoggedHours
        if event_type == "logged_hours":
            log: LoggedHours = data
            entry = ActivityHistory(
                student_id=log.student_id,
                activity_type="Hours Approved",
                description=f"{log.hours} hours approved by staff ID {log.staff_id}"
            )
            db.session.add(entry)
            db.session.commit()

        elif event_type == "accolade_awarded":
            student, accolade = data
            entry = ActivityHistory(
                student_id=student.student_id,
                activity_type="Accolade Earned",
                description=f"Accolade earned: {accolade}"
            )
            db.session.add(entry)
            db.session.commit()
