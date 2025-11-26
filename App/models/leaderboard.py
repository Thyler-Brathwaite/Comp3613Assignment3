from App.models.student import Student

class Leaderboard:
    def __init__(self, name: str):
        self.name = name
        self.students = [] 

    def update(self, student):
        
        if student not in self.students:
            self.students.append(student)

    def display(self):
       
        ranked = sorted(
            self.students,
            key=lambda s: s.total_hours,
            reverse=True
        )

        print(f"=== Leaderboard: {self.name} ===")
        for i, s in enumerate(ranked, start=1):
            print(f"{i}. {s.username} - {s.total_hours} hrs")

    def get_json(self):
      
        ranked = sorted(
            self.students,
            key=lambda s: s.total_hours,
            reverse=True
        )

        return [
            {
                'rank': i + 1,
                'student_id': s.student_id,
                'username': s.username,
                'total_hours': s.total_hours
            }
            for i, s in enumerate(ranked)
        ]

    def __repr__(self):
        return f"<Leaderboard: {self.name}>"
