from App.database import db

class Leaderboard(db.Model):
    __tablename__ = "leaderboard"


    name = db.Column(db.String(120), primary_key=True)
    students = db.Column(db.JSON, default=[])

    def __init__(self, name):
        self.name = name
        self.students = []

    def __repr__(self):
        return f"<Leaderboard {self.name} with {len(self.students)} students>"

    def get_json(self):
        return {
            "name": self.name,
            "students": self.students
        }
