from dataclasses import dataclass

@dataclass
class Student:
    name: str
    grade: float

students = [
    Student('A', 17.5),
    Student('C', 15),
    Student('B', 15)
]

# a complex sort leveled by 'grade', 'name', 'idx' (order)
decorated = [(student.grade, student.name, idx, student) for idx, student in enumerate(students)]
decorated.sort()
undecorated = [student for grade, name, idx, student in decorated]

print('students:', students)
print('undecorated:', undecorated)
