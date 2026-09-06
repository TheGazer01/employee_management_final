class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
 
student1 = Student("Juan", 20)
student2 = Student("Maria Santos", 19)
 
print("Student 1")
print("Name:", student1.name)
print("Age:", student1.age)
 
print()
 
print("Student 2")
print("Name:", student2.name)
print("Age:", student2.age)