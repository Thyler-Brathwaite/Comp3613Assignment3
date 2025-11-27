from App.database import db

class Accolade(db.Model):
    __tablename__ = "accolade"

    accolade_id= db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))

    def __init__(self, student_id, title, description=""):
        self.student_id = student_id
        self.title = title
        self.description = description

    def __repr__(self):
        return f"<Accolade {self.title} for Student {self.student_id}>"

    def get_json(self):
        return {
            "accolade_id": self.accolade_id,
            "student_id": self.student_id,
            "title": self.title,
            "description": self.description
        }
