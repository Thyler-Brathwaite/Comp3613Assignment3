from App.database import db
from App.models import Leaderboard
 

class LeaderboardController:
    
    def create_leaderboard(self, name):
        lb = Leaderboard(name=name)
        db.session.add(lb)
        db.session.commit()
        return lb

  
    def update(self, name, student_json):
    
        leaderboard = Leaderboard.query.get(name)
        if not leaderboard:
            return None

  
        for i, s in enumerate(leaderboard.students):
            if s["student_id"] == student_json["student_id"]:
                leaderboard.students[i] = student_json
                db.session.commit()
                return leaderboard


        leaderboard.students.append(student_json)
        db.session.commit()
        return leaderboard

 
    def display(self, name):
        leaderboard = Leaderboard.query.get(name)
        if not leaderboard:
            return "Leaderboard not found."

     
        print(f"=== Leaderboard: {leaderboard.name} ===")
        for i, s in enumerate(leaderboard.students, start=1):
            print(f"{i}. {s['name']} - {s['score']}")

        return leaderboard.students
