class InvalidAgeError(Exception):
    pass
 
class Person:
    def __init__(self, name, age):
        if age < 0:
            raise InvalidAgeError("Age cannot be negative.")
        self.name = name
        self.age = age
 
    def display_person_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
 
 
class Student(Person):
    school = "ABC College"
 
    def __init__(self, name, age, student_id, course, year_level):
        super().__init__(name, age)
        self.student_id = student_id
        self.course = course
        self.year_level = year_level
 
    def display_student_info(self):
        print()
        print("==============================")
        print("       STUDENT INFORMATION")
        print("==============================")
        self.display_person_info()
        print("Student ID:", self.student_id)
        print("Course:", self.course)
        print("Year Level:", self.year_level)
        print("School:", Student.school)
 
    def update_course(self, new_course):
        self.course = new_course
        print()
        print("Course successfully updated!")
 
 
try:
    print("==============================")
    print("STUDENT MANAGEMENT SYSTEM")
    print("==============================")
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    student_id = input("Enter Student ID: ")
    course = input("Enter course: ")
    year_level = int(input("Enter year level: "))
 
    student1 = Student(name, age, student_id, course, year_level)
    student1.display_student_info()
 
    print()
    print("==============================")
    print("               CLASS CHECK")
    print("==============================")
    print()
    print("Is student1 a Student?")
    print(isinstance(student1, Student))
    print()
    print("Is student1 a Person?")
    print(isinstance(student1, Person))
    print()
    print("Is Student a subclass of Person?")
    print(issubclass(Student, Person))
 
except ValueError:
    print()
    print("Error: Please enter a valid number.")
 
except InvalidAgeError as error:
    print()
    print("Error:", error)
 