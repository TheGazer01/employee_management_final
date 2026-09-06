class Student:
    def __init__(self, name):
        self.name = name
 
    def introduce(self):
        print("Hello!")
        print(" My name is ", self.name)
 
student1 = Student("juan Dela Cruz")
student1.introduce()
 