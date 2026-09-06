class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
 
class Student(Person):
    def __init__(self, name, age, student_id, course):
        super().__init__(name, age)
        self.student_id = student_id
        self.course = course
 
    def display_info(self):
        print("STUDENT INFORMATION")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Student ID:", self.student_id)
        print("Course:", self.course)
 
student1 = Student("Juan Dela Cruz", 20, "2026-001", "Computer Engineering")
student1.display_info()