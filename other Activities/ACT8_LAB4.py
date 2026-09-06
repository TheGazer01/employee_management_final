class Person:
    def introduce(self):
        print("I am a person.")

class Student(Person):
    pass

class Faculty:
    pass

class Administrator:
    pass

student1 = Student()
student1.introduce()

print("Checking Objects")
print()
print("Is student1 a Student?")
print(isinstance(student1, Student))
print()
print("Is student1 a Person?")
print(isinstance(student1, Person))
print()
print("Is student1 a Faculty?")
print(isinstance(student1, Faculty))
print()
print("Is student1 an Administrator?")
print(isinstance(student1, Administrator))
print()
print("Checking Classes")
print()
print("Is Student a subclass of Person?")
print(issubclass(Student, Person))
print()
print("Is Student a subclass of Faculty?")
print(issubclass(Student, Faculty))
print()
print("Is Student a subclass of Administrator?")
print(issubclass(Student, Administrator))